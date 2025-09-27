from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from src.models.user import User

def register_jwt_handlers(jwt):
    """Register JWT event handlers."""
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handle expired tokens."""
        return jsonify({
            'message': 'Token has expired',
            'error': 'token_expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid tokens."""
        return jsonify({
            'message': 'Invalid token',
            'error': 'invalid_token'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handle missing tokens."""
        return jsonify({
            'message': 'Authorization token is required',
            'error': 'authorization_required'
        }), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        """Handle non-fresh tokens."""
        return jsonify({
            'message': 'Fresh token required',
            'error': 'fresh_token_required'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Handle revoked tokens."""
        return jsonify({
            'message': 'Token has been revoked',
            'error': 'token_revoked'
        }), 401
    
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        """Define how to extract user identity from user object."""
        return str(user._id) if hasattr(user, '_id') else str(user)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Load user from JWT token."""
        identity = jwt_data["sub"]
        return User.find_by_id(identity)
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """Add additional claims to JWT token."""
        user = User.find_by_id(identity)
        if user:
            return {
                'role': user.role,
                'permissions': User.PERMISSIONS.get(user.role, []),
                'is_admin': user.role == 'admin'
            }
        return {}
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """Check if token is in blocklist (revoked)."""
        # This is a placeholder implementation
        # In production, you would check against a Redis cache or database
        # of revoked tokens
        jti = jwt_payload['jti']
        
        # For now, we'll assume no tokens are revoked
        # In production, implement proper token blacklisting
        return False
    
    @jwt.verify_jwt_in_request_loader
    def verify_jwt_in_request_callback(jwt_header, jwt_payload):
        """Custom JWT verification logic."""
        # Additional verification logic can be added here
        # For example, checking if user is still active
        user_id = jwt_payload.get('sub')
        if user_id:
            user = User.find_by_id(user_id)
            if not user or not user.is_active:
                return False
        return True
