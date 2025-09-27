from flask import Blueprint, request, jsonify
from src.middleware.auth import token_required, permission_required
from src.middleware.validation import validate_json, EnergyGridSchema, EnergyConsumptionSchema, RenewableEnergySchema
from src.models.energy import EnergyGrid, EnergyConsumption, RenewableEnergy, EnergyOptimization
from datetime import datetime, timedelta

energy_bp = Blueprint('energy', __name__)

@energy_bp.route('/grids', methods=['GET'])
@permission_required('energy.read')
def get_energy_grids(current_user):
    """Get energy grid data."""
    try:
        grid_id = request.args.get('grid_id')
        
        if grid_id:
            grid_data = EnergyGrid.get_latest_data(grid_id)
            return jsonify({'grid_data': format_grid_data(grid_data)}), 200
        else:
            grids_data = EnergyGrid.get_latest_data()
            return jsonify({
                'grids': [format_grid_data(grid['latest_data']) for grid in grids_data],
                'count': len(grids_data)
            }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get energy grids', 'error': str(e)}), 500

@energy_bp.route('/grids', methods=['POST'])
@permission_required('energy.write')
@validate_json(EnergyGridSchema)
def add_energy_grid_data(data, current_user):
    """Add new energy grid data."""
    try:
        grid = EnergyGrid(
            grid_id=data['grid_id'],
            grid_name=data['grid_name'],
            location=data['location'],
            capacity=data['capacity'],
            current_load=data['current_load'],
            voltage=data['voltage'],
            frequency=data['frequency'],
            status=data.get('status', 'operational')
        )
        
        grid_id = grid.save()
        
        # Check for alerts
        alerts = EnergyGrid.check_overload_alerts()
        if alerts:
            from app import socketio
            for alert in alerts:
                socketio.emit('energy_alert', alert, room='energy_monitoring')
        
        # Emit real-time update
        from app import socketio
        socketio.emit('energy_update', {
            'type': 'grid_update',
            'data': format_grid_data(grid.__dict__)
        }, room='energy_monitoring')
        
        return jsonify({
            'message': 'Energy grid data added successfully',
            'grid_id': grid_id,
            'alerts_triggered': len(alerts)
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to add energy grid data', 'error': str(e)}), 500

@energy_bp.route('/grids/load-distribution', methods=['GET'])
@permission_required('energy.read')
def get_load_distribution(current_user):
    """Get current load distribution across grids."""
    try:
        distribution = EnergyGrid.get_load_distribution()
        
        return jsonify({
            'load_distribution': distribution,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get load distribution', 'error': str(e)}), 500

@energy_bp.route('/consumption', methods=['GET'])
@permission_required('energy.read')
def get_energy_consumption(current_user):
    """Get energy consumption data."""
    try:
        consumer_type = request.args.get('type')
        
        if consumer_type:
            from app import mongo
            consumption_data = list(mongo.db.energy_consumption.find({'consumer_type': consumer_type}))
        else:
            consumption_data = EnergyConsumption.get_consumption_by_type()
        
        return jsonify({
            'consumption_data': consumption_data,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get consumption data', 'error': str(e)}), 500

@energy_bp.route('/consumption', methods=['POST'])
@permission_required('energy.write')
@validate_json(EnergyConsumptionSchema)
def add_consumption_data(data, current_user):
    """Add new energy consumption data."""
    try:
        consumption = EnergyConsumption(
            meter_id=data['meter_id'],
            location=data['location'],
            consumer_type=data['consumer_type'],
            consumption=data['consumption'],
            peak_demand=data['peak_demand'],
            cost=data['cost'],
            billing_period=data['billing_period']
        )
        
        consumption_id = consumption.save()
        
        return jsonify({
            'message': 'Consumption data added successfully',
            'consumption_id': consumption_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to add consumption data', 'error': str(e)}), 500

@energy_bp.route('/consumption/peak-demand', methods=['GET'])
@permission_required('energy.read')
def get_peak_demand_analysis(current_user):
    """Get peak demand analysis."""
    try:
        analysis = EnergyConsumption.get_peak_demand_analysis()
        
        return jsonify({
            'peak_demand_analysis': analysis,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get peak demand analysis', 'error': str(e)}), 500

@energy_bp.route('/renewable', methods=['GET'])
@permission_required('energy.read')
def get_renewable_energy(current_user):
    """Get renewable energy data."""
    try:
        source_type = request.args.get('type')
        
        if source_type:
            from app import mongo
            renewable_data = list(mongo.db.renewable_energy.find({'source_type': source_type}))
        else:
            renewable_data = RenewableEnergy.get_renewable_summary()
        
        return jsonify({
            'renewable_data': renewable_data,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get renewable energy data', 'error': str(e)}), 500

@energy_bp.route('/renewable', methods=['POST'])
@permission_required('energy.write')
@validate_json(RenewableEnergySchema)
def add_renewable_data(data, current_user):
    """Add new renewable energy data."""
    try:
        renewable = RenewableEnergy(
            source_id=data['source_id'],
            source_type=data['source_type'],
            location=data['location'],
            capacity=data['capacity'],
            current_generation=data['current_generation'],
            efficiency=data['efficiency'],
            weather_condition=data.get('weather_condition', 'clear')
        )
        
        renewable_id = renewable.save()
        
        # Emit real-time update
        from app import socketio
        socketio.emit('energy_update', {
            'type': 'renewable_update',
            'data': format_renewable_data(renewable.__dict__)
        }, room='energy_monitoring')
        
        return jsonify({
            'message': 'Renewable energy data added successfully',
            'renewable_id': renewable_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to add renewable energy data', 'error': str(e)}), 500

@energy_bp.route('/renewable/forecast', methods=['GET'])
@permission_required('energy.read')
def get_generation_forecast(current_user):
    """Get renewable energy generation forecast."""
    try:
        source_type = request.args.get('type')
        forecast = RenewableEnergy.get_generation_forecast(source_type)
        
        return jsonify({
            'generation_forecast': forecast,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get generation forecast', 'error': str(e)}), 500

@energy_bp.route('/optimization/load-balancing', methods=['GET'])
@permission_required('energy.read')
def get_load_optimization(current_user):
    """Get load balancing optimization recommendations."""
    try:
        optimization_plan = EnergyOptimization.optimize_load_distribution()
        
        return jsonify({
            'optimization_plan': optimization_plan,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get load optimization', 'error': str(e)}), 500

@energy_bp.route('/optimization/efficiency', methods=['GET'])
@permission_required('energy.read')
def get_efficiency_recommendations(current_user):
    """Get energy efficiency recommendations."""
    try:
        recommendations = EnergyOptimization.get_energy_efficiency_recommendations()
        
        return jsonify({
            'efficiency_recommendations': recommendations,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get efficiency recommendations', 'error': str(e)}), 500

@energy_bp.route('/alerts', methods=['GET'])
@permission_required('energy.read')
def get_energy_alerts(current_user):
    """Get energy system alerts."""
    try:
        alerts = EnergyGrid.check_overload_alerts()
        
        return jsonify({
            'alerts': alerts,
            'count': len(alerts),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get energy alerts', 'error': str(e)}), 500

@energy_bp.route('/dashboard', methods=['GET'])
@permission_required('energy.read')
def get_energy_dashboard(current_user):
    """Get energy management dashboard data."""
    try:
        # Get current grid status
        grids = EnergyGrid.get_latest_data()
        total_capacity = sum(grid['latest_data']['capacity'] for grid in grids)
        total_load = sum(grid['latest_data']['current_load'] for grid in grids)
        
        # Get renewable energy summary
        renewable_summary = RenewableEnergy.get_renewable_summary()
        total_renewable = sum(source['total_generation'] for source in renewable_summary)
        
        # Get consumption by type
        consumption_by_type = EnergyConsumption.get_consumption_by_type()
        
        # Get alerts
        alerts = EnergyGrid.check_overload_alerts()
        
        dashboard_data = {
            'grid_overview': {
                'total_capacity': total_capacity,
                'current_load': total_load,
                'load_percentage': (total_load / total_capacity * 100) if total_capacity > 0 else 0,
                'operational_grids': len([g for g in grids if g['latest_data']['status'] == 'operational'])
            },
            'renewable_energy': {
                'total_generation': total_renewable,
                'sources': renewable_summary,
                'renewable_percentage': (total_renewable / total_load * 100) if total_load > 0 else 0
            },
            'consumption': {
                'by_type': consumption_by_type,
                'total_consumption': sum(c['total_consumption'] for c in consumption_by_type)
            },
            'alerts': {
                'active_alerts': len(alerts),
                'critical_alerts': len([a for a in alerts if a['severity'] == 'critical']),
                'recent_alerts': alerts[:5]
            },
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(dashboard_data), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get energy dashboard', 'error': str(e)}), 500

@energy_bp.route('/reports/daily', methods=['GET'])
@permission_required('energy.read')
def get_daily_energy_report(current_user):
    """Get daily energy report."""
    try:
        today = datetime.now().date()
        
        # Get today's data
        from app import mongo
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        # Grid performance
        grid_data = list(mongo.db.energy_grids.find({
            'timestamp': {'$gte': start_of_day, '$lte': end_of_day}
        }))
        
        # Consumption data
        consumption_data = list(mongo.db.energy_consumption.find({
            'timestamp': {'$gte': start_of_day, '$lte': end_of_day}
        }))
        
        # Renewable generation
        renewable_data = list(mongo.db.renewable_energy.find({
            'timestamp': {'$gte': start_of_day, '$lte': end_of_day}
        }))
        
        report = {
            'date': today.isoformat(),
            'grid_performance': {
                'peak_load': max([g['current_load'] for g in grid_data]) if grid_data else 0,
                'average_load': sum([g['current_load'] for g in grid_data]) / len(grid_data) if grid_data else 0,
                'grid_efficiency': 95.5  # Placeholder calculation
            },
            'consumption': {
                'total_consumption': sum([c['consumption'] for c in consumption_data]),
                'peak_demand': max([c['peak_demand'] for c in consumption_data]) if consumption_data else 0,
                'total_cost': sum([c['cost'] for c in consumption_data])
            },
            'renewable_generation': {
                'total_generation': sum([r['current_generation'] for r in renewable_data]),
                'average_efficiency': sum([r['efficiency'] for r in renewable_data]) / len(renewable_data) if renewable_data else 0,
                'sources_active': len(set([r['source_type'] for r in renewable_data]))
            },
            'alerts': {
                'total_alerts': len(EnergyGrid.check_overload_alerts()),
                'resolved_alerts': 0  # Placeholder
            }
        }
        
        return jsonify(report), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to generate daily energy report', 'error': str(e)}), 500

# Helper functions
def format_grid_data(data):
    """Format grid data for API response."""
    return {
        'grid_id': data.get('grid_id'),
        'grid_name': data.get('grid_name'),
        'location': data.get('location'),
        'capacity': data.get('capacity'),
        'current_load': data.get('current_load'),
        'load_percentage': (data.get('current_load', 0) / data.get('capacity', 1)) * 100,
        'voltage': data.get('voltage'),
        'frequency': data.get('frequency'),
        'status': data.get('status'),
        'timestamp': data.get('timestamp').isoformat() if isinstance(data.get('timestamp'), datetime) else data.get('timestamp')
    }

def format_renewable_data(data):
    """Format renewable energy data for API response."""
    return {
        'source_id': data.get('source_id'),
        'source_type': data.get('source_type'),
        'location': data.get('location'),
        'capacity': data.get('capacity'),
        'current_generation': data.get('current_generation'),
        'generation_percentage': (data.get('current_generation', 0) / data.get('capacity', 1)) * 100,
        'efficiency': data.get('efficiency'),
        'weather_condition': data.get('weather_condition'),
        'timestamp': data.get('timestamp').isoformat() if isinstance(data.get('timestamp'), datetime) else data.get('timestamp')
    }
