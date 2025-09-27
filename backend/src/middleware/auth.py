from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from src.models.user import User

def token_required(f):
    """Decorator for routes that require authentication."""
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            current_user = User.find_by_id(current_user_id)
            
            if not current_user or not current_user.is_active:
                return jsonify({'message': 'User not found or inactive'}), 401
            
            return f(current_user, *args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token is invalid'}), 401
    
    return decorated

def role_required(*allowed_roles):
    """Decorator for routes that require specific roles."""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated(*args, **kwargs):
            try:
                current_user_id = get_jwt_identity()
                current_user = User.find_by_id(current_user_id)
                
                if not current_user or not current_user.is_active:
                    return jsonify({'message': 'User not found or inactive'}), 401
                
                if current_user.role not in allowed_roles and 'admin' not in allowed_roles:
                    if current_user.role != 'admin':  # Admin has access to everything
                        return jsonify({'message': 'Insufficient permissions'}), 403
                
                return f(current_user, *args, **kwargs)
            except Exception as e:
                return jsonify({'message': 'Authorization failed'}), 401
        
        return decorated
    return decorator

def permission_required(permission):
    """Decorator for routes that require specific permissions."""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated(*args, **kwargs):
            try:
                current_user_id = get_jwt_identity()
                current_user = User.find_by_id(current_user_id)
                
                if not current_user or not current_user.is_active:
                    return jsonify({'message': 'User not found or inactive'}), 401
                
                if not current_user.has_permission(permission):
                    return jsonify({'message': f'Permission {permission} required'}), 403
                
                return f(current_user, *args, **kwargs)
            except Exception as e:
                return jsonify({'message': 'Authorization failed'}), 401
        
        return decorated
    return decorator

def optional_auth(f):
    """Decorator for routes where authentication is optional."""
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
            current_user = None
            
            if current_user_id:
                current_user = User.find_by_id(current_user_id)
            
            return f(current_user, *args, **kwargs)
        except Exception:
            return f(None, *args, **kwargs)
    
    return decorated
