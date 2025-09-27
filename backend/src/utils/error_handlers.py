from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

def register_error_handlers(app):
    """Register error handlers for the Flask application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request could not be understood by the server',
            'status_code': 400
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors."""
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication is required to access this resource',
            'status_code': 401
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors."""
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource',
            'status_code': 403
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource could not be found',
            'status_code': 404
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for the requested URL',
            'status_code': 405
        }), 405
    
    @app.errorhandler(409)
    def conflict(error):
        """Handle 409 Conflict errors."""
        return jsonify({
            'error': 'Conflict',
            'message': 'The request could not be completed due to a conflict',
            'status_code': 409
        }), 409
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle 422 Unprocessable Entity errors."""
        return jsonify({
            'error': 'Unprocessable Entity',
            'message': 'The request was well-formed but contains semantic errors',
            'status_code': 422
        }), 422
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle 429 Too Many Requests errors."""
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later',
            'status_code': 429
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        app.logger.error(f'Internal Server Error: {error}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred on the server',
            'status_code': 500
        }), 500
    
    @app.errorhandler(502)
    def bad_gateway(error):
        """Handle 502 Bad Gateway errors."""
        return jsonify({
            'error': 'Bad Gateway',
            'message': 'The server received an invalid response from an upstream server',
            'status_code': 502
        }), 502
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle 503 Service Unavailable errors."""
        return jsonify({
            'error': 'Service Unavailable',
            'message': 'The server is temporarily unable to handle the request',
            'status_code': 503
        }), 503
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle all other HTTP exceptions."""
        return jsonify({
            'error': error.name,
            'message': error.description,
            'status_code': error.code
        }), error.code
    
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        """Handle all other exceptions."""
        app.logger.error(f'Unhandled Exception: {error}', exc_info=True)
        
        # Don't expose internal error details in production
        if app.config.get('DEBUG'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': str(error),
                'status_code': 500
            }), 500
        else:
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred',
                'status_code': 500
            }), 500
    
    # Custom error classes
    class ValidationError(Exception):
        """Custom validation error."""
        def __init__(self, message, status_code=400):
            self.message = message
            self.status_code = status_code
    
    class AuthenticationError(Exception):
        """Custom authentication error."""
        def __init__(self, message, status_code=401):
            self.message = message
            self.status_code = status_code
    
    class AuthorizationError(Exception):
        """Custom authorization error."""
        def __init__(self, message, status_code=403):
            self.message = message
            self.status_code = status_code
    
    class ResourceNotFoundError(Exception):
        """Custom resource not found error."""
        def __init__(self, message, status_code=404):
            self.message = message
            self.status_code = status_code
    
    class BusinessLogicError(Exception):
        """Custom business logic error."""
        def __init__(self, message, status_code=422):
            self.message = message
            self.status_code = status_code
    
    # Register custom error handlers
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            'error': 'Validation Error',
            'message': error.message,
            'status_code': error.status_code
        }), error.status_code
    
    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error):
        return jsonify({
            'error': 'Authentication Error',
            'message': error.message,
            'status_code': error.status_code
        }), error.status_code
    
    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(error):
        return jsonify({
            'error': 'Authorization Error',
            'message': error.message,
            'status_code': error.status_code
        }), error.status_code
    
    @app.errorhandler(ResourceNotFoundError)
    def handle_resource_not_found_error(error):
        return jsonify({
            'error': 'Resource Not Found',
            'message': error.message,
            'status_code': error.status_code
        }), error.status_code
    
    @app.errorhandler(BusinessLogicError)
    def handle_business_logic_error(error):
        return jsonify({
            'error': 'Business Logic Error',
            'message': error.message,
            'status_code': error.status_code
        }), error.status_code
