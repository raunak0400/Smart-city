from flask import Blueprint, jsonify
from src.middleware.auth import token_required, permission_required
from src.models.traffic import TrafficData, TrafficIncident
from src.models.environment import EnvironmentData
from src.models.waste import WasteBin, WasteCollection
from src.models.energy import EnergyGrid, EnergyConsumption, RenewableEnergy
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/overview', methods=['GET'])
@permission_required('dashboard.read')
def get_dashboard_overview(current_user):
    """Get dashboard overview with key metrics."""
    try:
        # Traffic metrics
        traffic_congestion = TrafficData.get_congestion_summary()
        active_incidents = len(TrafficIncident.get_active_incidents())
        
        # Environment metrics
        air_quality_summary = EnvironmentData.get_air_quality_summary()
        avg_aqi = sum(sensor['avg_aqi'] for sensor in air_quality_summary) / len(air_quality_summary) if air_quality_summary else 0
        
        # Waste metrics
        waste_stats = WasteBin.get_bin_statistics()
        full_bins = sum(stat['full_bins'] for stat in waste_stats)
        total_bins = sum(stat['total_bins'] for stat in waste_stats)
        
        # Energy metrics
        energy_load = EnergyGrid.get_load_distribution()
        total_capacity = sum(grid['capacity'] for grid in energy_load)
        total_load = sum(grid['current_load'] for grid in energy_load)
        load_percentage = (total_load / total_capacity * 100) if total_capacity > 0 else 0
        
        # Renewable energy
        renewable_summary = RenewableEnergy.get_renewable_summary()
        total_renewable = sum(source['total_generation'] for source in renewable_summary)
        
        overview = {
            'traffic': {
                'congestion_summary': traffic_congestion,
                'active_incidents': active_incidents,
                'status': 'normal' if active_incidents < 5 else 'alert'
            },
            'environment': {
                'average_aqi': round(avg_aqi, 2),
                'air_quality_status': get_aqi_status(avg_aqi),
                'sensor_count': len(air_quality_summary)
            },
            'waste': {
                'full_bins': full_bins,
                'total_bins': total_bins,
                'fill_percentage': round((full_bins / total_bins * 100) if total_bins > 0 else 0, 2),
                'status': 'normal' if full_bins < total_bins * 0.3 else 'alert'
            },
            'energy': {
                'load_percentage': round(load_percentage, 2),
                'total_capacity': total_capacity,
                'current_load': total_load,
                'renewable_generation': total_renewable,
                'status': 'normal' if load_percentage < 85 else 'alert'
            },
            'last_updated': datetime.utcnow().isoformat()
        }
        
        return jsonify(overview), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get dashboard overview', 'error': str(e)}), 500

@dashboard_bp.route('/real-time-data', methods=['GET'])
@permission_required('dashboard.read')
def get_real_time_data(current_user):
    """Get real-time data for dashboard widgets."""
    try:
        # Get latest data from each module
        latest_traffic = TrafficData.get_latest_data(limit=10)
        latest_environment = EnvironmentData.get_latest_data(limit=10)
        latest_energy = EnergyGrid.get_latest_data()
        
        # Format data for frontend
        real_time_data = {
            'traffic': {
                'latest_readings': [format_traffic_data(data) for data in latest_traffic],
                'timestamp': datetime.utcnow().isoformat()
            },
            'environment': {
                'latest_readings': [format_environment_data(data) for data in latest_environment],
                'timestamp': datetime.utcnow().isoformat()
            },
            'energy': {
                'grid_status': [format_energy_data(grid['latest_data']) for grid in latest_energy],
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        return jsonify(real_time_data), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get real-time data', 'error': str(e)}), 500

@dashboard_bp.route('/alerts/summary', methods=['GET'])
@permission_required('dashboard.read')
def get_alerts_summary(current_user):
    """Get summary of active alerts across all modules."""
    try:
        from src.models.environment import EnvironmentData
        
        alerts = []
        
        # Check traffic alerts
        incidents = TrafficIncident.get_active_incidents()
        for incident in incidents:
            alerts.append({
                'module': 'traffic',
                'type': incident['incident_type'],
                'severity': incident['severity'],
                'message': incident['description'],
                'location': incident['location'],
                'timestamp': incident['created_at']
            })
        
        # Check environment alerts
        env_alerts = EnvironmentData.check_pollution_alerts()
        alerts.extend(env_alerts)
        
        # Check energy alerts
        energy_alerts = EnergyGrid.check_overload_alerts()
        alerts.extend(energy_alerts)
        
        # Check waste alerts
        full_bins = WasteBin.get_full_bins(threshold=90)
        for bin_data in full_bins:
            alerts.append({
                'module': 'waste',
                'type': 'bin_full',
                'severity': 'medium',
                'message': f"Waste bin {bin_data['bin_id']} is {bin_data['current_level']}% full",
                'location': bin_data['location'],
                'timestamp': bin_data['updated_at']
            })
        
        # Sort alerts by severity and timestamp
        severity_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}
        alerts.sort(key=lambda x: (severity_order.get(x['severity'], 0), x['timestamp']), reverse=True)
        
        return jsonify({
            'alerts': alerts[:20],  # Return top 20 alerts
            'total_count': len(alerts),
            'critical_count': len([a for a in alerts if a['severity'] == 'critical']),
            'high_count': len([a for a in alerts if a['severity'] == 'high'])
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get alerts summary', 'error': str(e)}), 500

@dashboard_bp.route('/statistics/weekly', methods=['GET'])
@permission_required('dashboard.read')
def get_weekly_statistics(current_user):
    """Get weekly statistics for dashboard charts."""
    try:
        # Get data for the past 7 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        # Traffic statistics
        traffic_trends = get_traffic_weekly_trends(start_date, end_date)
        
        # Environment statistics
        pollution_trends = EnvironmentData.get_pollution_trends(days=7)
        
        # Energy statistics
        energy_trends = get_energy_weekly_trends(start_date, end_date)
        
        # Waste statistics
        waste_trends = get_waste_weekly_trends(start_date, end_date)
        
        weekly_stats = {
            'traffic': traffic_trends,
            'environment': pollution_trends,
            'energy': energy_trends,
            'waste': waste_trends,
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            }
        }
        
        return jsonify(weekly_stats), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get weekly statistics', 'error': str(e)}), 500

# Helper functions
def get_aqi_status(aqi):
    """Get air quality status based on AQI value."""
    if aqi <= 50:
        return 'good'
    elif aqi <= 100:
        return 'moderate'
    elif aqi <= 150:
        return 'unhealthy_sensitive'
    elif aqi <= 200:
        return 'unhealthy'
    elif aqi <= 300:
        return 'very_unhealthy'
    else:
        return 'hazardous'

def format_traffic_data(data):
    """Format traffic data for frontend."""
    return {
        'intersection_id': data['intersection_id'],
        'location': data['location'],
        'traffic_flow': data['traffic_flow'],
        'congestion_level': data['congestion_level'],
        'average_speed': data.get('average_speed', 0),
        'timestamp': data['timestamp'].isoformat() if isinstance(data['timestamp'], datetime) else data['timestamp']
    }

def format_environment_data(data):
    """Format environment data for frontend."""
    return {
        'sensor_id': data['sensor_id'],
        'location': data['location'],
        'air_quality_index': data['air_quality_index'],
        'pm25': data['pm25'],
        'temperature': data['temperature'],
        'humidity': data['humidity'],
        'timestamp': data['timestamp'].isoformat() if isinstance(data['timestamp'], datetime) else data['timestamp']
    }

def format_energy_data(data):
    """Format energy data for frontend."""
    return {
        'grid_id': data['grid_id'],
        'grid_name': data['grid_name'],
        'capacity': data['capacity'],
        'current_load': data['current_load'],
        'load_percentage': round((data['current_load'] / data['capacity']) * 100, 2),
        'status': data['status'],
        'timestamp': data['timestamp'].isoformat() if isinstance(data['timestamp'], datetime) else data['timestamp']
    }

def get_traffic_weekly_trends(start_date, end_date):
    """Get traffic trends for the past week."""
    from app import mongo
    
    pipeline = [
        {'$match': {'timestamp': {'$gte': start_date, '$lte': end_date}}},
        {
            '$group': {
                '_id': {
                    'year': {'$year': '$timestamp'},
                    'month': {'$month': '$timestamp'},
                    'day': {'$dayOfMonth': '$timestamp'}
                },
                'avg_flow': {'$avg': '$traffic_flow'},
                'incident_count': {'$sum': {'$cond': ['$incident_reported', 1, 0]}}
            }
        },
        {'$sort': {'_id': 1}}
    ]
    
    return list(mongo.db.traffic_data.aggregate(pipeline))

def get_energy_weekly_trends(start_date, end_date):
    """Get energy trends for the past week."""
    from app import mongo
    
    pipeline = [
        {'$match': {'timestamp': {'$gte': start_date, '$lte': end_date}}},
        {
            '$group': {
                '_id': {
                    'year': {'$year': '$timestamp'},
                    'month': {'$month': '$timestamp'},
                    'day': {'$dayOfMonth': '$timestamp'}
                },
                'avg_load': {'$avg': '$current_load'},
                'avg_capacity': {'$avg': '$capacity'}
            }
        },
        {'$sort': {'_id': 1}}
    ]
    
    return list(mongo.db.energy_grids.aggregate(pipeline))

def get_waste_weekly_trends(start_date, end_date):
    """Get waste trends for the past week."""
    from app import mongo
    
    pipeline = [
        {'$match': {'updated_at': {'$gte': start_date, '$lte': end_date}}},
        {
            '$group': {
                '_id': {
                    'year': {'$year': '$updated_at'},
                    'month': {'$month': '$updated_at'},
                    'day': {'$dayOfMonth': '$updated_at'}
                },
                'avg_fill_level': {'$avg': '$current_level'},
                'full_bins': {'$sum': {'$cond': [{'$gte': ['$current_level', 80]}, 1, 0]}}
            }
        },
        {'$sort': {'_id': 1}}
    ]
    
    return list(mongo.db.waste_bins.aggregate(pipeline))
