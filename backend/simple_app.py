#!/usr/bin/env python3
"""
Simple Flask app to test basic functionality with auth endpoints
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

def create_simple_app():
    """Create a simple Flask app for testing."""
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    # Enable CORS
    CORS(app)
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'message': 'Smart City Backend is running!'
        }), 200
    
    @app.route('/api/test', methods=['GET'])
    def test_endpoint():
        """Test endpoint."""
        return jsonify({
            'message': 'Backend is working!',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    # Auth endpoints for frontend compatibility
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """Simple login endpoint."""
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        # Simple validation - accept admin credentials
        if email == 'admin@smartcity.com' and password == 'admin123':
            return jsonify({
                'access_token': 'fake-jwt-token-for-testing',
                'user': {
                    'id': '1',
                    'email': 'admin@smartcity.com',
                    'name': 'Admin User',
                    'role': 'admin',
                    'permissions': ['all']
                }
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    
    @app.route('/api/auth/profile', methods=['GET'])
    def get_profile():
        """Simple profile endpoint."""
        # Check for authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Authorization required'}), 401
        
        return jsonify({
            'id': '1',
            'email': 'admin@smartcity.com',
            'name': 'Admin User',
            'role': 'admin',
            'permissions': ['all']
        }), 200
    
    # Dashboard endpoint
    @app.route('/api/dashboard/overview', methods=['GET'])
    def dashboard_overview():
        """Simple dashboard overview."""
        return jsonify({
            'total_alerts': 5,
            'active_incidents': 2,
            'system_status': 'operational',
            'last_updated': datetime.utcnow().isoformat()
        }), 200
    
    return app

if __name__ == '__main__':
    app = create_simple_app()
    print("🚀 Starting Simple Smart City Backend...")
    print("📍 Backend will be available at: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/api/health")
    print("🔐 Login: admin@smartcity.com / admin123")
    print("Press Ctrl+C to stop the server")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
