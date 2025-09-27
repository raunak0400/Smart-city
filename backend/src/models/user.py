from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo

class User:
    """User model for authentication and role management."""
    
    ROLES = {
        'admin': 'Administrator',
        'traffic_officer': 'Traffic Officer',
        'environment_officer': 'Environment Officer',
        'utility_officer': 'Utility Officer',
        'emergency_coordinator': 'Emergency Coordinator'
    }
    
    PERMISSIONS = {
        'admin': ['all'],
        'traffic_officer': ['traffic.read', 'traffic.write', 'dashboard.read'],
        'environment_officer': ['environment.read', 'environment.write', 'dashboard.read'],
        'utility_officer': ['waste.read', 'waste.write', 'energy.read', 'energy.write', 'dashboard.read'],
        'emergency_coordinator': ['emergency.read', 'emergency.write', 'alerts.read', 'alerts.write', 'dashboard.read']
    }
    
    def __init__(self, email, password, first_name, last_name, role='traffic_officer', 
                 phone=None, department=None, is_active=True):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.phone = phone
        self.department = department
        self.is_active = is_active
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.last_login = None
    
    def save(self):
        """Save user to database."""
        user_data = {
            'email': self.email,
            'password_hash': self.password_hash,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'phone': self.phone,
            'department': self.department,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_login': self.last_login
        }
        result = mongo.db.users.insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_email(email):
        """Find user by email."""
        user_data = mongo.db.users.find_one({'email': email})
        if user_data:
            user = User.__new__(User)
            user.__dict__.update(user_data)
            user._id = user_data['_id']
            return user
        return None
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID."""
        try:
            user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            if user_data:
                user = User.__new__(User)
                user.__dict__.update(user_data)
                user._id = user_data['_id']
                return user
        except:
            pass
        return None
    
    def check_password(self, password):
        """Check if provided password matches user's password."""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        mongo.db.users.update_one(
            {'_id': self._id},
            {'$set': {'last_login': self.last_login}}
        )
    
    def has_permission(self, permission):
        """Check if user has specific permission."""
        user_permissions = self.PERMISSIONS.get(self.role, [])
        return 'all' in user_permissions or permission in user_permissions
    
    def to_dict(self):
        """Convert user to dictionary for JSON serialization."""
        return {
            'id': str(self._id) if hasattr(self, '_id') else None,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'role_name': self.ROLES.get(self.role, self.role),
            'phone': self.phone,
            'department': self.department,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    @staticmethod
    def get_all_users():
        """Get all users."""
        users = []
        for user_data in mongo.db.users.find():
            user = User.__new__(User)
            user.__dict__.update(user_data)
            user._id = user_data['_id']
            users.append(user.to_dict())
        return users
