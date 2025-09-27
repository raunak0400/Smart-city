from flask import Blueprint, request, jsonify
from src.middleware.auth import token_required, permission_required
from src.middleware.validation import validate_json, AlertSchema
from datetime import datetime, timedelta
from bson import ObjectId

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/', methods=['GET'])
@permission_required('alerts.read')
def get_alerts(current_user):
    """Get alerts with filtering options."""
    try:
        # Query parameters
        status = request.args.get('status', 'active')
        severity = request.args.get('severity')
        module = request.args.get('module')
        limit = int(request.args.get('limit', 50))
        
        from app import mongo
        
        # Build query
        query = {}
        if status:
            query['status'] = status
        if severity:
            query['severity'] = severity
        if module:
            query['module'] = module
        
        alerts = list(mongo.db.alerts.find(query).sort('created_at', -1).limit(limit))
        
        return jsonify({
            'alerts': [format_alert(alert) for alert in alerts],
            'count': len(alerts),
            'filters': {
                'status': status,
                'severity': severity,
                'module': module
            }
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get alerts', 'error': str(e)}), 500

@alerts_bp.route('/', methods=['POST'])
@permission_required('alerts.write')
@validate_json(AlertSchema)
def create_alert(data, current_user):
    """Create a new alert."""
    try:
        alert_data = {
            'alert_type': data['alert_type'],
            'severity': data['severity'],
            'message': data['message'],
            'module': data['module'],
            'threshold_value': data.get('threshold_value'),
            'current_value': data.get('current_value'),
            'location': data.get('location'),
            'affected_systems': data.get('affected_systems', []),
            'recommended_actions': data.get('recommended_actions', []),
            'status': 'active',
            'created_by': str(current_user._id),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'acknowledged_by': None,
            'acknowledged_at': None,
            'resolved_by': None,
            'resolved_at': None
        }
        
        from app import mongo
        result = mongo.db.alerts.insert_one(alert_data)
        
        # Emit real-time alert
        from app import socketio
        socketio.emit('new_alert', {
            'alert': format_alert(alert_data),
            'alert_id': str(result.inserted_id)
        }, room='alerts')
        
        # Send notifications based on severity
        if data['severity'] in ['high', 'critical']:
            send_alert_notifications(alert_data, str(result.inserted_id))
        
        return jsonify({
            'message': 'Alert created successfully',
            'alert_id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to create alert', 'error': str(e)}), 500

@alerts_bp.route('/<alert_id>/acknowledge', methods=['PUT'])
@permission_required('alerts.write')
def acknowledge_alert(current_user, alert_id):
    """Acknowledge an alert."""
    try:
        from app import mongo
        
        # Update alert
        result = mongo.db.alerts.update_one(
            {'_id': ObjectId(alert_id)},
            {
                '$set': {
                    'status': 'acknowledged',
                    'acknowledged_by': str(current_user._id),
                    'acknowledged_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            return jsonify({'message': 'Alert not found'}), 404
        
        # Emit real-time update
        from app import socketio
        socketio.emit('alert_acknowledged', {
            'alert_id': alert_id,
            'acknowledged_by': str(current_user._id),
            'acknowledged_at': datetime.utcnow().isoformat()
        }, room='alerts')
        
        return jsonify({'message': 'Alert acknowledged successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to acknowledge alert', 'error': str(e)}), 500

@alerts_bp.route('/<alert_id>/resolve', methods=['PUT'])
@permission_required('alerts.write')
def resolve_alert(current_user, alert_id):
    """Resolve an alert."""
    try:
        data = request.get_json()
        resolution_notes = data.get('resolution_notes', '')
        
        from app import mongo
        
        # Update alert
        result = mongo.db.alerts.update_one(
            {'_id': ObjectId(alert_id)},
            {
                '$set': {
                    'status': 'resolved',
                    'resolved_by': str(current_user._id),
                    'resolved_at': datetime.utcnow(),
                    'resolution_notes': resolution_notes,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            return jsonify({'message': 'Alert not found'}), 404
        
        # Emit real-time update
        from app import socketio
        socketio.emit('alert_resolved', {
            'alert_id': alert_id,
            'resolved_by': str(current_user._id),
            'resolved_at': datetime.utcnow().isoformat()
        }, room='alerts')
        
        return jsonify({'message': 'Alert resolved successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to resolve alert', 'error': str(e)}), 500

@alerts_bp.route('/bulk-acknowledge', methods=['PUT'])
@permission_required('alerts.write')
def bulk_acknowledge_alerts(current_user):
    """Acknowledge multiple alerts."""
    try:
        data = request.get_json()
        alert_ids = data.get('alert_ids', [])
        
        if not alert_ids:
            return jsonify({'message': 'No alert IDs provided'}), 400
        
        from app import mongo
        
        # Convert string IDs to ObjectIds
        object_ids = [ObjectId(aid) for aid in alert_ids]
        
        # Update alerts
        result = mongo.db.alerts.update_many(
            {'_id': {'$in': object_ids}, 'status': 'active'},
            {
                '$set': {
                    'status': 'acknowledged',
                    'acknowledged_by': str(current_user._id),
                    'acknowledged_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        # Emit real-time update
        from app import socketio
        socketio.emit('alerts_bulk_acknowledged', {
            'alert_ids': alert_ids,
            'acknowledged_by': str(current_user._id),
            'count': result.modified_count
        }, room='alerts')
        
        return jsonify({
            'message': f'{result.modified_count} alerts acknowledged successfully',
            'acknowledged_count': result.modified_count
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to acknowledge alerts', 'error': str(e)}), 500

@alerts_bp.route('/statistics', methods=['GET'])
@permission_required('alerts.read')
def get_alert_statistics(current_user):
    """Get alert statistics."""
    try:
        days = int(request.args.get('days', 30))
        start_date = datetime.utcnow() - timedelta(days=days)
        
        from app import mongo
        
        # Alert counts by status
        status_pipeline = [
            {'$match': {'created_at': {'$gte': start_date}}},
            {
                '$group': {
                    '_id': '$status',
                    'count': {'$sum': 1}
                }
            }
        ]
        status_stats = list(mongo.db.alerts.aggregate(status_pipeline))
        
        # Alert counts by severity
        severity_pipeline = [
            {'$match': {'created_at': {'$gte': start_date}}},
            {
                '$group': {
                    '_id': '$severity',
                    'count': {'$sum': 1}
                }
            }
        ]
        severity_stats = list(mongo.db.alerts.aggregate(severity_pipeline))
        
        # Alert counts by module
        module_pipeline = [
            {'$match': {'created_at': {'$gte': start_date}}},
            {
                '$group': {
                    '_id': '$module',
                    'count': {'$sum': 1}
                }
            }
        ]
        module_stats = list(mongo.db.alerts.aggregate(module_pipeline))
        
        # Response time analysis
        response_time_pipeline = [
            {
                '$match': {
                    'created_at': {'$gte': start_date},
                    'acknowledged_at': {'$exists': True}
                }
            },
            {
                '$project': {
                    'response_time_minutes': {
                        '$divide': [
                            {'$subtract': ['$acknowledged_at', '$created_at']},
                            60000  # Convert to minutes
                        ]
                    },
                    'severity': 1
                }
            },
            {
                '$group': {
                    '_id': '$severity',
                    'avg_response_time': {'$avg': '$response_time_minutes'},
                    'count': {'$sum': 1}
                }
            }
        ]
        response_time_stats = list(mongo.db.alerts.aggregate(response_time_pipeline))
        
        # Daily alert trends
        daily_trends_pipeline = [
            {'$match': {'created_at': {'$gte': start_date}}},
            {
                '$group': {
                    '_id': {
                        'year': {'$year': '$created_at'},
                        'month': {'$month': '$created_at'},
                        'day': {'$dayOfMonth': '$created_at'}
                    },
                    'total_alerts': {'$sum': 1},
                    'critical_alerts': {
                        '$sum': {'$cond': [{'$eq': ['$severity', 'critical']}, 1, 0]}
                    },
                    'high_alerts': {
                        '$sum': {'$cond': [{'$eq': ['$severity', 'high']}, 1, 0]}
                    }
                }
            },
            {'$sort': {'_id': 1}}
        ]
        daily_trends = list(mongo.db.alerts.aggregate(daily_trends_pipeline))
        
        statistics = {
            'period_days': days,
            'status_distribution': {stat['_id']: stat['count'] for stat in status_stats},
            'severity_distribution': {stat['_id']: stat['count'] for stat in severity_stats},
            'module_distribution': {stat['_id']: stat['count'] for stat in module_stats},
            'response_times': response_time_stats,
            'daily_trends': daily_trends,
            'total_alerts': sum(stat['count'] for stat in status_stats),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(statistics), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get alert statistics', 'error': str(e)}), 500

@alerts_bp.route('/rules', methods=['GET'])
@permission_required('alerts.read')
def get_alert_rules(current_user):
    """Get alert rules configuration."""
    try:
        from app import mongo
        
        rules = list(mongo.db.alert_rules.find())
        
        return jsonify({
            'alert_rules': [format_alert_rule(rule) for rule in rules],
            'count': len(rules)
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get alert rules', 'error': str(e)}), 500

@alerts_bp.route('/rules', methods=['POST'])
@permission_required('alerts.write')
def create_alert_rule(current_user):
    """Create a new alert rule."""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'module', 'condition', 'threshold', 'severity']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        rule_data = {
            'name': data['name'],
            'description': data.get('description', ''),
            'module': data['module'],
            'condition': data['condition'],  # greater_than, less_than, equals, contains
            'threshold': data['threshold'],
            'severity': data['severity'],
            'enabled': data.get('enabled', True),
            'notification_channels': data.get('notification_channels', ['email']),
            'cooldown_minutes': data.get('cooldown_minutes', 60),
            'created_by': str(current_user._id),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        from app import mongo
        result = mongo.db.alert_rules.insert_one(rule_data)
        
        return jsonify({
            'message': 'Alert rule created successfully',
            'rule_id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to create alert rule', 'error': str(e)}), 500

@alerts_bp.route('/rules/<rule_id>', methods=['PUT'])
@permission_required('alerts.write')
def update_alert_rule(current_user, rule_id):
    """Update an alert rule."""
    try:
        data = request.get_json()
        
        update_data = {
            'updated_at': datetime.utcnow()
        }
        
        allowed_fields = ['name', 'description', 'condition', 'threshold', 'severity', 'enabled', 'notification_channels', 'cooldown_minutes']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        from app import mongo
        result = mongo.db.alert_rules.update_one(
            {'_id': ObjectId(rule_id)},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({'message': 'Alert rule not found'}), 404
        
        return jsonify({'message': 'Alert rule updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to update alert rule', 'error': str(e)}), 500

@alerts_bp.route('/rules/<rule_id>', methods=['DELETE'])
@permission_required('alerts.write')
def delete_alert_rule(current_user, rule_id):
    """Delete an alert rule."""
    try:
        from app import mongo
        
        result = mongo.db.alert_rules.delete_one({'_id': ObjectId(rule_id)})
        
        if result.deleted_count == 0:
            return jsonify({'message': 'Alert rule not found'}), 404
        
        return jsonify({'message': 'Alert rule deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to delete alert rule', 'error': str(e)}), 500

@alerts_bp.route('/notifications/settings', methods=['GET'])
@permission_required('alerts.read')
def get_notification_settings(current_user):
    """Get notification settings for current user."""
    try:
        from app import mongo
        
        settings = mongo.db.notification_settings.find_one({'user_id': str(current_user._id)})
        
        if not settings:
            # Default settings
            settings = {
                'user_id': str(current_user._id),
                'email_enabled': True,
                'sms_enabled': False,
                'push_enabled': True,
                'severity_filter': ['high', 'critical'],
                'module_filter': [],
                'quiet_hours': {'start': '22:00', 'end': '06:00'},
                'created_at': datetime.utcnow()
            }
        
        return jsonify(format_notification_settings(settings)), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get notification settings', 'error': str(e)}), 500

@alerts_bp.route('/notifications/settings', methods=['PUT'])
@permission_required('alerts.write')
def update_notification_settings(current_user):
    """Update notification settings for current user."""
    try:
        data = request.get_json()
        
        settings_data = {
            'user_id': str(current_user._id),
            'email_enabled': data.get('email_enabled', True),
            'sms_enabled': data.get('sms_enabled', False),
            'push_enabled': data.get('push_enabled', True),
            'severity_filter': data.get('severity_filter', ['high', 'critical']),
            'module_filter': data.get('module_filter', []),
            'quiet_hours': data.get('quiet_hours', {'start': '22:00', 'end': '06:00'}),
            'updated_at': datetime.utcnow()
        }
        
        from app import mongo
        mongo.db.notification_settings.update_one(
            {'user_id': str(current_user._id)},
            {'$set': settings_data},
            upsert=True
        )
        
        return jsonify({'message': 'Notification settings updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to update notification settings', 'error': str(e)}), 500

# Helper functions
def format_alert(data):
    """Format alert data for API response."""
    return {
        'id': str(data.get('_id', '')),
        'alert_type': data.get('alert_type'),
        'severity': data.get('severity'),
        'message': data.get('message'),
        'module': data.get('module'),
        'threshold_value': data.get('threshold_value'),
        'current_value': data.get('current_value'),
        'location': data.get('location'),
        'affected_systems': data.get('affected_systems', []),
        'recommended_actions': data.get('recommended_actions', []),
        'status': data.get('status'),
        'created_by': data.get('created_by'),
        'created_at': data.get('created_at').isoformat() if isinstance(data.get('created_at'), datetime) else data.get('created_at'),
        'acknowledged_by': data.get('acknowledged_by'),
        'acknowledged_at': data.get('acknowledged_at').isoformat() if data.get('acknowledged_at') and isinstance(data.get('acknowledged_at'), datetime) else data.get('acknowledged_at'),
        'resolved_by': data.get('resolved_by'),
        'resolved_at': data.get('resolved_at').isoformat() if data.get('resolved_at') and isinstance(data.get('resolved_at'), datetime) else data.get('resolved_at'),
        'resolution_notes': data.get('resolution_notes')
    }

def format_alert_rule(data):
    """Format alert rule data for API response."""
    return {
        'id': str(data.get('_id', '')),
        'name': data.get('name'),
        'description': data.get('description'),
        'module': data.get('module'),
        'condition': data.get('condition'),
        'threshold': data.get('threshold'),
        'severity': data.get('severity'),
        'enabled': data.get('enabled'),
        'notification_channels': data.get('notification_channels', []),
        'cooldown_minutes': data.get('cooldown_minutes'),
        'created_by': data.get('created_by'),
        'created_at': data.get('created_at').isoformat() if isinstance(data.get('created_at'), datetime) else data.get('created_at')
    }

def format_notification_settings(data):
    """Format notification settings for API response."""
    return {
        'user_id': data.get('user_id'),
        'email_enabled': data.get('email_enabled'),
        'sms_enabled': data.get('sms_enabled'),
        'push_enabled': data.get('push_enabled'),
        'severity_filter': data.get('severity_filter', []),
        'module_filter': data.get('module_filter', []),
        'quiet_hours': data.get('quiet_hours', {})
    }

def send_alert_notifications(alert_data, alert_id):
    """Send alert notifications via configured channels."""
    # This is a placeholder for actual notification implementation
    # In production, integrate with email, SMS, and push notification services
    pass
