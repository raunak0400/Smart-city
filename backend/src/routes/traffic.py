from flask import Blueprint, request, jsonify
from src.middleware.auth import token_required, permission_required
from src.middleware.validation import validate_json, TrafficDataSchema, TrafficIncidentSchema
from src.models.traffic import TrafficData, TrafficIncident
from datetime import datetime, timedelta

traffic_bp = Blueprint('traffic', __name__)

@traffic_bp.route('/data', methods=['GET'])
@permission_required('traffic.read')
def get_traffic_data(current_user):
    """Get traffic data with optional filtering."""
    try:
        intersection_id = request.args.get('intersection_id')
        limit = int(request.args.get('limit', 100))
        
        traffic_data = TrafficData.get_latest_data(intersection_id, limit)
        
        return jsonify({
            'traffic_data': [format_traffic_data(data) for data in traffic_data],
            'count': len(traffic_data)
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get traffic data', 'error': str(e)}), 500

@traffic_bp.route('/data', methods=['POST'])
@permission_required('traffic.write')
@validate_json(TrafficDataSchema)
def add_traffic_data(data, current_user):
    """Add new traffic data."""
    try:
        traffic = TrafficData(
            intersection_id=data['intersection_id'],
            location=data['location'],
            traffic_flow=data['traffic_flow'],
            congestion_level=data['congestion_level'],
            signal_timing=data.get('signal_timing'),
            vehicle_count=data.get('vehicle_count'),
            average_speed=data.get('average_speed'),
            incident_reported=data.get('incident_reported', False),
            weather_condition=data.get('weather_condition', 'clear')
        )
        
        traffic_id = traffic.save()
        
        # Emit real-time update via WebSocket
        from app import socketio
        socketio.emit('traffic_update', {
            'type': 'new_data',
            'data': format_traffic_data(traffic.__dict__)
        }, room='traffic_monitoring')
        
        return jsonify({
            'message': 'Traffic data added successfully',
            'traffic_id': traffic_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to add traffic data', 'error': str(e)}), 500

@traffic_bp.route('/congestion/summary', methods=['GET'])
@permission_required('traffic.read')
def get_congestion_summary(current_user):
    """Get traffic congestion summary."""
    try:
        summary = TrafficData.get_congestion_summary()
        
        return jsonify({
            'congestion_summary': summary,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get congestion summary', 'error': str(e)}), 500

@traffic_bp.route('/peak-hours', methods=['GET'])
@permission_required('traffic.read')
def get_peak_hours_analysis(current_user):
    """Get peak hours traffic analysis."""
    try:
        analysis = TrafficData.get_peak_hours_analysis()
        
        return jsonify({
            'peak_hours_analysis': analysis,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get peak hours analysis', 'error': str(e)}), 500

@traffic_bp.route('/incidents', methods=['GET'])
@permission_required('traffic.read')
def get_incidents(current_user):
    """Get traffic incidents."""
    try:
        status = request.args.get('status', 'active')
        
        if status == 'active':
            incidents = TrafficIncident.get_active_incidents()
        else:
            from app import mongo
            incidents = list(mongo.db.traffic_incidents.find({'status': status}))
        
        return jsonify({
            'incidents': [format_incident_data(incident) for incident in incidents],
            'count': len(incidents)
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get incidents', 'error': str(e)}), 500

@traffic_bp.route('/incidents', methods=['POST'])
@permission_required('traffic.write')
@validate_json(TrafficIncidentSchema)
def report_incident(data, current_user):
    """Report a new traffic incident."""
    try:
        incident = TrafficIncident(
            location=data['location'],
            incident_type=data['incident_type'],
            severity=data['severity'],
            description=data['description'],
            reported_by=str(current_user._id)
        )
        
        incident_id = incident.save()
        
        # Emit real-time alert
        from app import socketio
        socketio.emit('traffic_alert', {
            'type': 'new_incident',
            'incident': format_incident_data(incident.__dict__)
        }, room='traffic_monitoring')
        
        return jsonify({
            'message': 'Incident reported successfully',
            'incident_id': incident_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to report incident', 'error': str(e)}), 500

@traffic_bp.route('/incidents/<incident_id>/resolve', methods=['PUT'])
@permission_required('traffic.write')
def resolve_incident(current_user, incident_id):
    """Resolve a traffic incident."""
    try:
        TrafficIncident.resolve_incident(incident_id)
        
        # Emit real-time update
        from app import socketio
        socketio.emit('traffic_alert', {
            'type': 'incident_resolved',
            'incident_id': incident_id
        }, room='traffic_monitoring')
        
        return jsonify({'message': 'Incident resolved successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to resolve incident', 'error': str(e)}), 500

@traffic_bp.route('/optimization/signals', methods=['GET'])
@permission_required('traffic.read')
def get_signal_optimization(current_user):
    """Get traffic signal optimization recommendations."""
    try:
        # Get current traffic data for all intersections
        traffic_data = TrafficData.get_latest_data(limit=50)
        
        recommendations = []
        
        for data in traffic_data:
            if data['congestion_level'] in ['high', 'critical']:
                # Calculate optimal signal timing based on traffic flow
                optimal_timing = calculate_optimal_signal_timing(data)
                
                recommendations.append({
                    'intersection_id': data['intersection_id'],
                    'location': data['location'],
                    'current_timing': data.get('signal_timing', {}),
                    'recommended_timing': optimal_timing,
                    'congestion_level': data['congestion_level'],
                    'traffic_flow': data['traffic_flow'],
                    'priority': 'high' if data['congestion_level'] == 'critical' else 'medium'
                })
        
        return jsonify({
            'signal_recommendations': recommendations,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get signal optimization', 'error': str(e)}), 500

@traffic_bp.route('/optimization/routes', methods=['POST'])
@permission_required('traffic.read')
def get_route_optimization(current_user):
    """Get route optimization for emergency vehicles."""
    try:
        data = request.get_json()
        start_location = data.get('start_location')
        end_location = data.get('end_location')
        vehicle_type = data.get('vehicle_type', 'emergency')
        
        if not start_location or not end_location:
            return jsonify({'message': 'Start and end locations are required'}), 400
        
        # Get current traffic conditions
        traffic_data = TrafficData.get_latest_data(limit=100)
        
        # Simple route optimization (in production, use proper routing algorithms)
        optimized_route = optimize_emergency_route(start_location, end_location, traffic_data)
        
        return jsonify({
            'optimized_route': optimized_route,
            'estimated_time': optimized_route.get('estimated_time', 0),
            'alternative_routes': optimized_route.get('alternatives', []),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to optimize route', 'error': str(e)}), 500

@traffic_bp.route('/analytics/flow-patterns', methods=['GET'])
@permission_required('traffic.read')
def get_flow_patterns(current_user):
    """Get traffic flow pattern analysis."""
    try:
        days = int(request.args.get('days', 7))
        
        # Get traffic flow patterns
        from app import mongo
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {'$match': {'timestamp': {'$gte': start_date}}},
            {
                '$group': {
                    '_id': {
                        'intersection_id': '$intersection_id',
                        'hour': {'$hour': '$timestamp'},
                        'day_of_week': {'$dayOfWeek': '$timestamp'}
                    },
                    'avg_flow': {'$avg': '$traffic_flow'},
                    'avg_speed': {'$avg': '$average_speed'},
                    'congestion_frequency': {
                        '$avg': {
                            '$switch': {
                                'branches': [
                                    {'case': {'$eq': ['$congestion_level', 'low']}, 'then': 1},
                                    {'case': {'$eq': ['$congestion_level', 'medium']}, 'then': 2},
                                    {'case': {'$eq': ['$congestion_level', 'high']}, 'then': 3},
                                    {'case': {'$eq': ['$congestion_level', 'critical']}, 'then': 4}
                                ],
                                'default': 1
                            }
                        }
                    }
                }
            },
            {'$sort': {'_id.intersection_id': 1, '_id.day_of_week': 1, '_id.hour': 1}}
        ]
        
        patterns = list(mongo.db.traffic_data.aggregate(pipeline))
        
        return jsonify({
            'flow_patterns': patterns,
            'analysis_period': f'{days} days',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get flow patterns', 'error': str(e)}), 500

# Helper functions
def format_traffic_data(data):
    """Format traffic data for API response."""
    return {
        'intersection_id': data.get('intersection_id'),
        'location': data.get('location'),
        'traffic_flow': data.get('traffic_flow'),
        'congestion_level': data.get('congestion_level'),
        'signal_timing': data.get('signal_timing'),
        'vehicle_count': data.get('vehicle_count'),
        'average_speed': data.get('average_speed'),
        'incident_reported': data.get('incident_reported'),
        'weather_condition': data.get('weather_condition'),
        'timestamp': data.get('timestamp').isoformat() if isinstance(data.get('timestamp'), datetime) else data.get('timestamp')
    }

def format_incident_data(data):
    """Format incident data for API response."""
    return {
        'id': str(data.get('_id', '')),
        'location': data.get('location'),
        'incident_type': data.get('incident_type'),
        'severity': data.get('severity'),
        'description': data.get('description'),
        'reported_by': data.get('reported_by'),
        'status': data.get('status'),
        'created_at': data.get('created_at').isoformat() if isinstance(data.get('created_at'), datetime) else data.get('created_at'),
        'updated_at': data.get('updated_at').isoformat() if isinstance(data.get('updated_at'), datetime) else data.get('updated_at'),
        'resolved_at': data.get('resolved_at').isoformat() if data.get('resolved_at') and isinstance(data.get('resolved_at'), datetime) else data.get('resolved_at')
    }

def calculate_optimal_signal_timing(traffic_data):
    """Calculate optimal signal timing based on traffic flow."""
    base_green = 45
    base_red = 30
    base_yellow = 5
    
    flow = traffic_data['traffic_flow']
    congestion = traffic_data['congestion_level']
    
    # Adjust timing based on traffic flow and congestion
    if congestion == 'critical':
        green_time = min(base_green + 20, 90)
        red_time = max(base_red - 10, 20)
    elif congestion == 'high':
        green_time = min(base_green + 10, 75)
        red_time = max(base_red - 5, 25)
    else:
        green_time = base_green
        red_time = base_red
    
    return {
        'green': green_time,
        'yellow': base_yellow,
        'red': red_time,
        'cycle_time': green_time + base_yellow + red_time
    }

def optimize_emergency_route(start, end, traffic_data):
    """Optimize route for emergency vehicles (simplified implementation)."""
    # This is a simplified implementation
    # In production, integrate with proper routing services like Google Maps API
    
    # Calculate base route time
    base_time = 15  # minutes (placeholder)
    
    # Adjust for traffic conditions
    high_congestion_areas = [data for data in traffic_data if data['congestion_level'] in ['high', 'critical']]
    
    # Simple penalty for congested areas
    congestion_penalty = len(high_congestion_areas) * 2
    
    estimated_time = base_time + congestion_penalty
    
    return {
        'route_points': [start, end],  # Simplified
        'estimated_time': estimated_time,
        'distance': 10.5,  # km (placeholder)
        'traffic_conditions': 'moderate',
        'alternatives': [
            {
                'route_points': [start, end],
                'estimated_time': estimated_time + 5,
                'distance': 12.0,
                'traffic_conditions': 'light'
            }
        ]
    }
