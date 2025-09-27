from flask import Blueprint, request, jsonify
from src.middleware.auth import token_required, permission_required
from src.middleware.validation import validate_json
from datetime import datetime, timedelta
from bson import ObjectId

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.route('/incidents', methods=['GET'])
@permission_required('emergency.read')
def get_emergency_incidents(current_user):
    """Get emergency incidents."""
    try:
        status = request.args.get('status', 'active')
        severity = request.args.get('severity')
        limit = int(request.args.get('limit', 50))
        
        from app import mongo
        query = {}
        if status:
            query['status'] = status
        if severity:
            query['severity'] = severity
        
        incidents = list(mongo.db.emergency_incidents.find(query).sort('created_at', -1).limit(limit))
        
        return jsonify({
            'incidents': [format_emergency_incident(incident) for incident in incidents],
            'count': len(incidents)
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get emergency incidents', 'error': str(e)}), 500

@emergency_bp.route('/incidents', methods=['POST'])
@permission_required('emergency.write')
def create_emergency_incident(current_user):
    """Create a new emergency incident."""
    try:
        data = request.get_json()
        
        required_fields = ['incident_type', 'severity', 'location', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        incident_data = {
            'incident_type': data['incident_type'],  # fire, medical, accident, natural_disaster, security
            'severity': data['severity'],  # low, medium, high, critical
            'location': data['location'],
            'description': data['description'],
            'reported_by': str(current_user._id),
            'status': 'active',
            'assigned_units': data.get('assigned_units', []),
            'estimated_response_time': data.get('estimated_response_time'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'resolved_at': None
        }
        
        from app import mongo
        result = mongo.db.emergency_incidents.insert_one(incident_data)
        
        # Emit real-time alert
        from app import socketio
        socketio.emit('emergency_alert', {
            'type': 'new_incident',
            'incident': format_emergency_incident(incident_data),
            'incident_id': str(result.inserted_id)
        }, room='emergency_response')
        
        # Auto-dispatch based on severity
        if data['severity'] in ['high', 'critical']:
            dispatch_emergency_units(str(result.inserted_id), data['incident_type'], data['location'])
        
        return jsonify({
            'message': 'Emergency incident created successfully',
            'incident_id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to create emergency incident', 'error': str(e)}), 500

@emergency_bp.route('/incidents/<incident_id>/update', methods=['PUT'])
@permission_required('emergency.write')
def update_emergency_incident(current_user, incident_id):
    """Update an emergency incident."""
    try:
        data = request.get_json()
        
        update_data = {
            'updated_at': datetime.utcnow()
        }
        
        allowed_fields = ['status', 'assigned_units', 'description', 'severity']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        if data.get('status') == 'resolved':
            update_data['resolved_at'] = datetime.utcnow()
        
        from app import mongo
        mongo.db.emergency_incidents.update_one(
            {'_id': ObjectId(incident_id)},
            {'$set': update_data}
        )
        
        # Emit real-time update
        from app import socketio
        socketio.emit('emergency_update', {
            'type': 'incident_updated',
            'incident_id': incident_id,
            'updates': update_data
        }, room='emergency_response')
        
        return jsonify({'message': 'Emergency incident updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to update emergency incident', 'error': str(e)}), 500

@emergency_bp.route('/units', methods=['GET'])
@permission_required('emergency.read')
def get_emergency_units(current_user):
    """Get emergency response units."""
    try:
        unit_type = request.args.get('type')
        status = request.args.get('status')
        
        from app import mongo
        query = {}
        if unit_type:
            query['unit_type'] = unit_type
        if status:
            query['status'] = status
        
        units = list(mongo.db.emergency_units.find(query))
        
        return jsonify({
            'units': [format_emergency_unit(unit) for unit in units],
            'count': len(units)
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get emergency units', 'error': str(e)}), 500

@emergency_bp.route('/units', methods=['POST'])
@permission_required('emergency.write')
def add_emergency_unit(current_user):
    """Add a new emergency unit."""
    try:
        data = request.get_json()
        
        required_fields = ['unit_id', 'unit_type', 'location', 'crew_members']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        unit_data = {
            'unit_id': data['unit_id'],
            'unit_type': data['unit_type'],  # fire_truck, ambulance, police_car, rescue_team
            'location': data['location'],
            'crew_members': data['crew_members'],
            'equipment': data.get('equipment', []),
            'status': data.get('status', 'available'),  # available, dispatched, busy, maintenance
            'current_incident': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        from app import mongo
        result = mongo.db.emergency_units.insert_one(unit_data)
        
        return jsonify({
            'message': 'Emergency unit added successfully',
            'unit_id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to add emergency unit', 'error': str(e)}), 500

@emergency_bp.route('/units/<unit_id>/dispatch', methods=['PUT'])
@permission_required('emergency.write')
def dispatch_unit(current_user, unit_id):
    """Dispatch an emergency unit to an incident."""
    try:
        data = request.get_json()
        incident_id = data.get('incident_id')
        
        if not incident_id:
            return jsonify({'message': 'incident_id is required'}), 400
        
        from app import mongo
        
        # Update unit status
        mongo.db.emergency_units.update_one(
            {'_id': ObjectId(unit_id)},
            {
                '$set': {
                    'status': 'dispatched',
                    'current_incident': incident_id,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        # Update incident with assigned unit
        mongo.db.emergency_incidents.update_one(
            {'_id': ObjectId(incident_id)},
            {
                '$addToSet': {'assigned_units': unit_id},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        # Emit real-time update
        from app import socketio
        socketio.emit('emergency_update', {
            'type': 'unit_dispatched',
            'unit_id': unit_id,
            'incident_id': incident_id
        }, room='emergency_response')
        
        return jsonify({'message': 'Unit dispatched successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to dispatch unit', 'error': str(e)}), 500

@emergency_bp.route('/response-plan', methods=['POST'])
@permission_required('emergency.write')
def create_response_plan(current_user):
    """Create an emergency response plan."""
    try:
        data = request.get_json()
        
        required_fields = ['incident_id', 'response_strategy', 'required_units']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        plan_data = {
            'incident_id': data['incident_id'],
            'response_strategy': data['response_strategy'],
            'required_units': data['required_units'],
            'evacuation_zones': data.get('evacuation_zones', []),
            'resource_allocation': data.get('resource_allocation', {}),
            'communication_plan': data.get('communication_plan', {}),
            'estimated_duration': data.get('estimated_duration'),
            'created_by': str(current_user._id),
            'status': 'active',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        from app import mongo
        result = mongo.db.emergency_response_plans.insert_one(plan_data)
        
        return jsonify({
            'message': 'Response plan created successfully',
            'plan_id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to create response plan', 'error': str(e)}), 500

@emergency_bp.route('/alerts/broadcast', methods=['POST'])
@permission_required('emergency.write')
def broadcast_emergency_alert(current_user):
    """Broadcast emergency alert to citizens."""
    try:
        data = request.get_json()
        
        required_fields = ['alert_type', 'message', 'affected_areas']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} is required'}), 400
        
        alert_data = {
            'alert_type': data['alert_type'],  # evacuation, shelter, weather, security
            'message': data['message'],
            'affected_areas': data['affected_areas'],
            'severity': data.get('severity', 'medium'),
            'instructions': data.get('instructions', ''),
            'contact_info': data.get('contact_info', ''),
            'broadcast_channels': data.get('broadcast_channels', ['sms', 'email', 'app']),
            'created_by': str(current_user._id),
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(hours=data.get('duration_hours', 24))
        }
        
        from app import mongo
        result = mongo.db.emergency_alerts.insert_one(alert_data)
        
        # Emit real-time alert
        from app import socketio
        socketio.emit('public_emergency_alert', {
            'alert': alert_data,
            'alert_id': str(result.inserted_id)
        }, room='public_alerts')
        
        # Here you would integrate with SMS, email, and push notification services
        send_emergency_notifications(alert_data)
        
        return jsonify({
            'message': 'Emergency alert broadcasted successfully',
            'alert_id': str(result.inserted_id)
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to broadcast alert', 'error': str(e)}), 500

@emergency_bp.route('/dashboard', methods=['GET'])
@permission_required('emergency.read')
def get_emergency_dashboard(current_user):
    """Get emergency management dashboard data."""
    try:
        from app import mongo
        
        # Active incidents
        active_incidents = list(mongo.db.emergency_incidents.find({'status': 'active'}))
        
        # Available units
        available_units = list(mongo.db.emergency_units.find({'status': 'available'}))
        dispatched_units = list(mongo.db.emergency_units.find({'status': 'dispatched'}))
        
        # Recent alerts
        recent_alerts = list(mongo.db.emergency_alerts.find().sort('created_at', -1).limit(5))
        
        # Response time analytics
        resolved_incidents = list(mongo.db.emergency_incidents.find({
            'status': 'resolved',
            'resolved_at': {'$exists': True},
            'created_at': {'$gte': datetime.utcnow() - timedelta(days=30)}
        }))
        
        avg_response_time = 0
        if resolved_incidents:
            response_times = []
            for incident in resolved_incidents:
                if incident.get('resolved_at') and incident.get('created_at'):
                    response_time = (incident['resolved_at'] - incident['created_at']).total_seconds() / 60
                    response_times.append(response_time)
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        dashboard_data = {
            'incidents': {
                'active': len(active_incidents),
                'critical': len([i for i in active_incidents if i['severity'] == 'critical']),
                'high': len([i for i in active_incidents if i['severity'] == 'high']),
                'recent_incidents': [format_emergency_incident(i) for i in active_incidents[:5]]
            },
            'units': {
                'total': len(available_units) + len(dispatched_units),
                'available': len(available_units),
                'dispatched': len(dispatched_units),
                'by_type': get_units_by_type()
            },
            'response_metrics': {
                'avg_response_time_minutes': round(avg_response_time, 2),
                'incidents_resolved_today': len([i for i in resolved_incidents if i['resolved_at'].date() == datetime.now().date()]),
                'response_efficiency': 85.5  # Placeholder calculation
            },
            'alerts': {
                'active_alerts': len([a for a in recent_alerts if a['expires_at'] > datetime.utcnow()]),
                'recent_alerts': [format_emergency_alert(a) for a in recent_alerts]
            },
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(dashboard_data), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get emergency dashboard', 'error': str(e)}), 500

@emergency_bp.route('/statistics/response-times', methods=['GET'])
@permission_required('emergency.read')
def get_response_time_statistics(current_user):
    """Get response time statistics."""
    try:
        days = int(request.args.get('days', 30))
        start_date = datetime.utcnow() - timedelta(days=days)
        
        from app import mongo
        pipeline = [
            {
                '$match': {
                    'status': 'resolved',
                    'created_at': {'$gte': start_date},
                    'resolved_at': {'$exists': True}
                }
            },
            {
                '$project': {
                    'incident_type': 1,
                    'severity': 1,
                    'response_time_minutes': {
                        '$divide': [
                            {'$subtract': ['$resolved_at', '$created_at']},
                            60000  # Convert to minutes
                        ]
                    }
                }
            },
            {
                '$group': {
                    '_id': {
                        'incident_type': '$incident_type',
                        'severity': '$severity'
                    },
                    'avg_response_time': {'$avg': '$response_time_minutes'},
                    'min_response_time': {'$min': '$response_time_minutes'},
                    'max_response_time': {'$max': '$response_time_minutes'},
                    'incident_count': {'$sum': 1}
                }
            }
        ]
        
        statistics = list(mongo.db.emergency_incidents.aggregate(pipeline))
        
        return jsonify({
            'response_time_statistics': statistics,
            'period_days': days,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get response time statistics', 'error': str(e)}), 500

# Helper functions
def format_emergency_incident(data):
    """Format emergency incident for API response."""
    return {
        'id': str(data.get('_id', '')),
        'incident_type': data.get('incident_type'),
        'severity': data.get('severity'),
        'location': data.get('location'),
        'description': data.get('description'),
        'reported_by': data.get('reported_by'),
        'status': data.get('status'),
        'assigned_units': data.get('assigned_units', []),
        'estimated_response_time': data.get('estimated_response_time'),
        'created_at': data.get('created_at').isoformat() if isinstance(data.get('created_at'), datetime) else data.get('created_at'),
        'updated_at': data.get('updated_at').isoformat() if isinstance(data.get('updated_at'), datetime) else data.get('updated_at'),
        'resolved_at': data.get('resolved_at').isoformat() if data.get('resolved_at') and isinstance(data.get('resolved_at'), datetime) else data.get('resolved_at')
    }

def format_emergency_unit(data):
    """Format emergency unit for API response."""
    return {
        'id': str(data.get('_id', '')),
        'unit_id': data.get('unit_id'),
        'unit_type': data.get('unit_type'),
        'location': data.get('location'),
        'crew_members': data.get('crew_members'),
        'equipment': data.get('equipment', []),
        'status': data.get('status'),
        'current_incident': data.get('current_incident'),
        'created_at': data.get('created_at').isoformat() if isinstance(data.get('created_at'), datetime) else data.get('created_at')
    }

def format_emergency_alert(data):
    """Format emergency alert for API response."""
    return {
        'id': str(data.get('_id', '')),
        'alert_type': data.get('alert_type'),
        'message': data.get('message'),
        'affected_areas': data.get('affected_areas'),
        'severity': data.get('severity'),
        'instructions': data.get('instructions'),
        'created_at': data.get('created_at').isoformat() if isinstance(data.get('created_at'), datetime) else data.get('created_at'),
        'expires_at': data.get('expires_at').isoformat() if isinstance(data.get('expires_at'), datetime) else data.get('expires_at')
    }

def dispatch_emergency_units(incident_id, incident_type, location):
    """Auto-dispatch emergency units based on incident type."""
    from app import mongo
    
    # Define unit requirements by incident type
    unit_requirements = {
        'fire': ['fire_truck'],
        'medical': ['ambulance'],
        'accident': ['ambulance', 'police_car'],
        'natural_disaster': ['rescue_team', 'fire_truck'],
        'security': ['police_car']
    }
    
    required_units = unit_requirements.get(incident_type, ['police_car'])
    
    for unit_type in required_units:
        # Find nearest available unit
        available_unit = mongo.db.emergency_units.find_one({
            'unit_type': unit_type,
            'status': 'available'
        })
        
        if available_unit:
            # Dispatch the unit
            mongo.db.emergency_units.update_one(
                {'_id': available_unit['_id']},
                {
                    '$set': {
                        'status': 'dispatched',
                        'current_incident': incident_id,
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            
            # Update incident
            mongo.db.emergency_incidents.update_one(
                {'_id': ObjectId(incident_id)},
                {'$addToSet': {'assigned_units': str(available_unit['_id'])}}
            )

def get_units_by_type():
    """Get unit count by type."""
    from app import mongo
    
    pipeline = [
        {
            '$group': {
                '_id': '$unit_type',
                'total': {'$sum': 1},
                'available': {
                    '$sum': {'$cond': [{'$eq': ['$status', 'available']}, 1, 0]}
                },
                'dispatched': {
                    '$sum': {'$cond': [{'$eq': ['$status', 'dispatched']}, 1, 0]}
                }
            }
        }
    ]
    
    return list(mongo.db.emergency_units.aggregate(pipeline))

def send_emergency_notifications(alert_data):
    """Send emergency notifications via various channels."""
    # This is a placeholder for actual notification implementation
    # In production, integrate with SMS, email, and push notification services
    pass
