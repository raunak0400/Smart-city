from flask import Blueprint, request, jsonify
from src.middleware.auth import token_required, permission_required
from src.middleware.validation import validate_json, EnvironmentDataSchema
from src.models.environment import EnvironmentData, EnvironmentAlert
from datetime import datetime, timedelta

environment_bp = Blueprint('environment', __name__)

@environment_bp.route('/data', methods=['GET'])
@permission_required('environment.read')
def get_environment_data(current_user):
    """Get environmental monitoring data."""
    try:
        sensor_id = request.args.get('sensor_id')
        limit = int(request.args.get('limit', 100))
        
        env_data = EnvironmentData.get_latest_data(sensor_id, limit)
        
        return jsonify({
            'environment_data': [format_environment_data(data) for data in env_data],
            'count': len(env_data)
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get environment data', 'error': str(e)}), 500

@environment_bp.route('/data', methods=['POST'])
@permission_required('environment.write')
@validate_json(EnvironmentDataSchema)
def add_environment_data(data, current_user):
    """Add new environmental data."""
    try:
        env_data = EnvironmentData(
            sensor_id=data['sensor_id'],
            location=data['location'],
            air_quality_index=data['air_quality_index'],
            pm25=data['pm25'],
            pm10=data['pm10'],
            co2_level=data['co2_level'],
            noise_level=data['noise_level'],
            temperature=data['temperature'],
            humidity=data['humidity'],
            weather_condition=data.get('weather_condition', 'clear')
        )
        
        env_id = env_data.save()
        
        # Check for alerts
        alerts = EnvironmentData.check_pollution_alerts()
        if alerts:
            from app import socketio
            for alert in alerts:
                socketio.emit('environment_alert', alert, room='environment_monitoring')
        
        # Emit real-time update
        from app import socketio
        socketio.emit('environment_update', {
            'type': 'new_data',
            'data': format_environment_data(env_data.__dict__)
        }, room='environment_monitoring')
        
        return jsonify({
            'message': 'Environment data added successfully',
            'environment_id': env_id,
            'alerts_triggered': len(alerts)
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to add environment data', 'error': str(e)}), 500

@environment_bp.route('/air-quality/summary', methods=['GET'])
@permission_required('environment.read')
def get_air_quality_summary(current_user):
    """Get air quality summary by sensors."""
    try:
        summary = EnvironmentData.get_air_quality_summary()
        
        return jsonify({
            'air_quality_summary': summary,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get air quality summary', 'error': str(e)}), 500

@environment_bp.route('/pollution/trends', methods=['GET'])
@permission_required('environment.read')
def get_pollution_trends(current_user):
    """Get pollution trends over specified period."""
    try:
        days = int(request.args.get('days', 7))
        trends = EnvironmentData.get_pollution_trends(days)
        
        return jsonify({
            'pollution_trends': trends,
            'period_days': days,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get pollution trends', 'error': str(e)}), 500

@environment_bp.route('/alerts', methods=['GET'])
@permission_required('environment.read')
def get_environment_alerts(current_user):
    """Get environmental alerts."""
    try:
        status = request.args.get('status', 'active')
        
        if status == 'active':
            alerts = EnvironmentAlert.get_active_alerts()
        else:
            from app import mongo
            alerts = list(mongo.db.environment_alerts.find({'status': status}))
        
        return jsonify({
            'alerts': [format_alert_data(alert) for alert in alerts],
            'count': len(alerts)
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get environment alerts', 'error': str(e)}), 500

@environment_bp.route('/alerts/<alert_id>/acknowledge', methods=['PUT'])
@permission_required('environment.write')
def acknowledge_alert(current_user, alert_id):
    """Acknowledge an environmental alert."""
    try:
        EnvironmentAlert.acknowledge_alert(alert_id, str(current_user._id))
        
        return jsonify({'message': 'Alert acknowledged successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to acknowledge alert', 'error': str(e)}), 500

# Helper functions
def format_environment_data(data):
    """Format environment data for API response."""
    return {
        'sensor_id': data.get('sensor_id'),
        'location': data.get('location'),
        'air_quality_index': data.get('air_quality_index'),
        'pm25': data.get('pm25'),
        'pm10': data.get('pm10'),
        'co2_level': data.get('co2_level'),
        'noise_level': data.get('noise_level'),
        'temperature': data.get('temperature'),
        'humidity': data.get('humidity'),
        'weather_condition': data.get('weather_condition'),
        'timestamp': data.get('timestamp').isoformat() if isinstance(data.get('timestamp'), datetime) else data.get('timestamp')
    }

def format_alert_data(data):
    """Format alert data for API response."""
    return {
        'id': str(data.get('_id', '')),
        'alert_type': data.get('alert_type'),
        'severity': data.get('severity'),
        'message': data.get('message'),
        'sensor_id': data.get('sensor_id'),
        'threshold_value': data.get('threshold_value'),
        'current_value': data.get('current_value'),
        'status': data.get('status'),
        'created_at': data.get('created_at').isoformat() if isinstance(data.get('created_at'), datetime) else data.get('created_at'),
        'acknowledged_by': data.get('acknowledged_by')
    }
