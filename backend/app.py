from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config
from datetime import datetime
import os

# Initialize extensions
mongo = PyMongo()
jwt = JWTManager()
socketio = SocketIO()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    
    # Initialize CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from src.routes.auth import auth_bp
    from src.routes.dashboard import dashboard_bp
    from src.routes.traffic import traffic_bp
    from src.routes.environment import environment_bp
    from src.routes.waste import waste_bp
    from src.routes.energy import energy_bp
    from src.routes.emergency import emergency_bp
    from src.routes.analytics import analytics_bp
    from src.routes.alerts import alerts_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(traffic_bp, url_prefix='/api/traffic')
    app.register_blueprint(environment_bp, url_prefix='/api/environment')
    app.register_blueprint(waste_bp, url_prefix='/api/waste')
    app.register_blueprint(energy_bp, url_prefix='/api/energy')
    app.register_blueprint(emergency_bp, url_prefix='/api/emergency')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    
    # Register error handlers
    from src.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Register JWT handlers
    from src.utils.jwt_handlers import register_jwt_handlers
    register_jwt_handlers(jwt)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint for monitoring."""
        try:
            # Test database connection
            mongo.db.command('ping')
            
            return {
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'version': '1.0.0',
                'services': {
                    'database': 'connected',
                    'application': 'running'
                }
            }, 200
        except Exception as e:
            return {
                'status': 'unhealthy',
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }, 503
    
    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
