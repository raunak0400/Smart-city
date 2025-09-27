from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.models.user import User
from src.middleware.validation import validate_json, UserRegistrationSchema, UserLoginSchema
from src.middleware.auth import token_required, role_required
from app import limiter
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
@role_required('admin')  # Only admin can register new users
@validate_json(UserRegistrationSchema)
def register(data, current_user):
    """Register a new user."""
    try:
        # Check if user already exists
        if User.find_by_email(data['email']):
            return jsonify({'message': 'Email already registered'}), 400
        
        # Validate password strength
        password = data['password']
        if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password):
            return jsonify({
                'message': 'Password must contain at least one uppercase letter, one lowercase letter, and one digit'
            }), 400
        
        # Create new user
        user = User(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data['role'],
            phone=data.get('phone'),
            department=data.get('department')
        )
        
        user_id = user.save()
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
@validate_json(UserLoginSchema)
def login(data):
    """User login."""
    try:
        user = User.find_by_email(data['email'])
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'message': 'Account is deactivated'}), 401
        
        # Update last login
        user.update_last_login()
        
        # Create tokens
        access_token = create_access_token(identity=str(user._id))
        refresh_token = create_refresh_token(identity=str(user._id))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    try:
        current_user_id = get_jwt_identity()
        user = User.find_by_id(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'message': 'User not found or inactive'}), 401
        
        new_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': new_token
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Token refresh failed', 'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get current user profile."""
    try:
        return jsonify({
            'user': current_user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get profile', 'error': str(e)}), 500

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update current user profile."""
    try:
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['first_name', 'last_name', 'phone', 'department']
        update_data = {}
        
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        if update_data:
            from app import mongo
            mongo.db.users.update_one(
                {'_id': current_user._id},
                {'$set': update_data}
            )
        
        # Get updated user
        updated_user = User.find_by_id(str(current_user._id))
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': updated_user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Profile update failed', 'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    """Change user password."""
    try:
        data = request.get_json()
        
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'message': 'Current password and new password are required'}), 400
        
        # Verify current password
        if not current_user.check_password(data['current_password']):
            return jsonify({'message': 'Current password is incorrect'}), 400
        
        # Validate new password
        new_password = data['new_password']
        if len(new_password) < 8:
            return jsonify({'message': 'New password must be at least 8 characters long'}), 400
        
        if not re.search(r'[A-Z]', new_password) or not re.search(r'[a-z]', new_password) or not re.search(r'\d', new_password):
            return jsonify({
                'message': 'New password must contain at least one uppercase letter, one lowercase letter, and one digit'
            }), 400
        
        # Update password
        from werkzeug.security import generate_password_hash
        from app import mongo
        
        mongo.db.users.update_one(
            {'_id': current_user._id},
            {'$set': {'password_hash': generate_password_hash(new_password)}}
        )
        
        return jsonify({'message': 'Password changed successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Password change failed', 'error': str(e)}), 500

@auth_bp.route('/users', methods=['GET'])
@role_required('admin')
def get_all_users(current_user):
    """Get all users (admin only)."""
    try:
        users = User.get_all_users()
        return jsonify({'users': users}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get users', 'error': str(e)}), 500

@auth_bp.route('/users/<user_id>/toggle-status', methods=['PUT'])
@role_required('admin')
def toggle_user_status(current_user, user_id):
    """Toggle user active status (admin only)."""
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        from app import mongo
        new_status = not user.is_active
        
        mongo.db.users.update_one(
            {'_id': user._id},
            {'$set': {'is_active': new_status}}
        )
        
        return jsonify({
            'message': f"User {'activated' if new_status else 'deactivated'} successfully"
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to toggle user status', 'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """User logout (client should discard token)."""
    return jsonify({'message': 'Logout successful'}), 200
