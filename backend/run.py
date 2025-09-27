#!/usr/bin/env python3
"""
Smart City Management Platform - Backend Server
Production-ready Flask application with WebSocket support
"""

import os
import sys
from app import create_app, socketio
from src.utils.helpers import setup_logging

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Main entry point for the application."""
    
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create Flask application
    app = create_app(config_name)
    
    # Setup logging
    setup_logging(app)
    
    # Import WebSocket handlers
    from src.utils import websocket_handlers
    
    # Get host and port from environment or use defaults
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = config_name == 'development'
    
    app.logger.info(f'Starting Smart City Management Platform on {host}:{port}')
    app.logger.info(f'Configuration: {config_name}')
    app.logger.info(f'Debug mode: {debug}')
    
    try:
        # Run the application with SocketIO
        socketio.run(
            app,
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug,
            log_output=True
        )
    except KeyboardInterrupt:
        app.logger.info('Application stopped by user')
    except Exception as e:
        app.logger.error(f'Application failed to start: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
