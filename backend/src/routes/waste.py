from flask import Blueprint, request, jsonify
from src.middleware.auth import token_required, permission_required
from src.middleware.validation import validate_json, WasteBinSchema, WasteCollectionSchema
from src.models.waste import WasteBin, WasteCollection, WasteAnalytics
from datetime import datetime, timedelta

waste_bp = Blueprint('waste', __name__)

@waste_bp.route('/bins', methods=['GET'])
@permission_required('waste.read')
def get_waste_bins(current_user):
    """Get all waste bins with optional filtering."""
    try:
        bin_type = request.args.get('type')
        status = request.args.get('status')
        threshold = int(request.args.get('threshold', 0))
        
        if threshold > 0:
            bins = WasteBin.get_full_bins(threshold)
        else:
            bins = WasteBin.get_all_bins()
        
        # Apply filters
        if bin_type:
            bins = [bin for bin in bins if bin['bin_type'] == bin_type]
        if status:
            bins = [bin for bin in bins if bin['status'] == status]
        
        return jsonify({
            'waste_bins': [format_bin_data(bin) for bin in bins],
            'count': len(bins)
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get waste bins', 'error': str(e)}), 500

@waste_bp.route('/bins', methods=['POST'])
@permission_required('waste.write')
@validate_json(WasteBinSchema)
def add_waste_bin(data, current_user):
    """Add a new waste bin."""
    try:
        waste_bin = WasteBin(
            bin_id=data['bin_id'],
            location=data['location'],
            bin_type=data['bin_type'],
            capacity=data['capacity'],
            current_level=data.get('current_level', 0)
        )
        
        bin_id = waste_bin.save()
        
        return jsonify({
            'message': 'Waste bin added successfully',
            'bin_id': bin_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to add waste bin', 'error': str(e)}), 500

@waste_bp.route('/bins/<bin_id>/update-level', methods=['PUT'])
@permission_required('waste.write')
def update_bin_level(current_user, bin_id):
    """Update waste bin fill level."""
    try:
        data = request.get_json()
        level = data.get('level')
        
        if level is None or not (0 <= level <= 100):
            return jsonify({'message': 'Level must be between 0 and 100'}), 400
        
        WasteBin.update_level(bin_id, level)
        
        # Check if bin needs collection
        if level >= 80:
            from app import socketio
            socketio.emit('waste_alert', {
                'type': 'bin_full',
                'bin_id': bin_id,
                'level': level,
                'message': f'Bin {bin_id} is {level}% full and needs collection'
            }, room='waste_monitoring')
        
        return jsonify({'message': 'Bin level updated successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to update bin level', 'error': str(e)}), 500

@waste_bp.route('/bins/<bin_id>/empty', methods=['PUT'])
@permission_required('waste.write')
def empty_bin(current_user, bin_id):
    """Mark bin as emptied."""
    try:
        WasteBin.empty_bin(bin_id)
        
        # Emit real-time update
        from app import socketio
        socketio.emit('waste_update', {
            'type': 'bin_emptied',
            'bin_id': bin_id,
            'timestamp': datetime.utcnow().isoformat()
        }, room='waste_monitoring')
        
        return jsonify({'message': 'Bin marked as emptied'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to empty bin', 'error': str(e)}), 500

@waste_bp.route('/bins/statistics', methods=['GET'])
@permission_required('waste.read')
def get_bin_statistics(current_user):
    """Get waste bin statistics."""
    try:
        stats = WasteBin.get_bin_statistics()
        
        return jsonify({
            'bin_statistics': stats,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get bin statistics', 'error': str(e)}), 500

@waste_bp.route('/collections', methods=['GET'])
@permission_required('waste.read')
def get_collections(current_user):
    """Get waste collection schedules."""
    try:
        date_filter = request.args.get('date', 'today')
        
        if date_filter == 'today':
            collections = WasteCollection.get_today_collections()
        else:
            from app import mongo
            collections = list(mongo.db.waste_collections.find().sort('scheduled_time', -1).limit(50))
        
        return jsonify({
            'collections': [format_collection_data(collection) for collection in collections],
            'count': len(collections)
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get collections', 'error': str(e)}), 500

@waste_bp.route('/collections', methods=['POST'])
@permission_required('waste.write')
@validate_json(WasteCollectionSchema)
def schedule_collection(data, current_user):
    """Schedule a new waste collection."""
    try:
        collection = WasteCollection(
            route_id=data['route_id'],
            route_name=data['route_name'],
            assigned_vehicle=data['assigned_vehicle'],
            assigned_crew=data['assigned_crew'],
            scheduled_time=data['scheduled_time'],
            bin_ids=data['bin_ids']
        )
        
        collection_id = collection.save()
        
        return jsonify({
            'message': 'Collection scheduled successfully',
            'collection_id': collection_id
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to schedule collection', 'error': str(e)}), 500

@waste_bp.route('/collections/<collection_id>/start', methods=['PUT'])
@permission_required('waste.write')
def start_collection(current_user, collection_id):
    """Start a collection route."""
    try:
        WasteCollection.start_collection(collection_id)
        
        # Emit real-time update
        from app import socketio
        socketio.emit('waste_update', {
            'type': 'collection_started',
            'collection_id': collection_id,
            'timestamp': datetime.utcnow().isoformat()
        }, room='waste_monitoring')
        
        return jsonify({'message': 'Collection started successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to start collection', 'error': str(e)}), 500

@waste_bp.route('/collections/<collection_id>/complete', methods=['PUT'])
@permission_required('waste.write')
def complete_collection(current_user, collection_id):
    """Complete a collection route."""
    try:
        WasteCollection.complete_collection(collection_id)
        
        # Mark all bins in route as emptied
        from app import mongo
        collection = mongo.db.waste_collections.find_one({'_id': ObjectId(collection_id)})
        if collection:
            for bin_id in collection['bin_ids']:
                WasteBin.empty_bin(bin_id)
        
        # Emit real-time update
        from app import socketio
        socketio.emit('waste_update', {
            'type': 'collection_completed',
            'collection_id': collection_id,
            'timestamp': datetime.utcnow().isoformat()
        }, room='waste_monitoring')
        
        return jsonify({'message': 'Collection completed successfully'}), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to complete collection', 'error': str(e)}), 500

@waste_bp.route('/optimization/routes', methods=['POST'])
@permission_required('waste.read')
def optimize_collection_routes(current_user):
    """Optimize waste collection routes."""
    try:
        data = request.get_json()
        bin_ids = data.get('bin_ids', [])
        
        if not bin_ids:
            # Get all bins that need collection
            full_bins = WasteBin.get_full_bins(threshold=70)
            bin_ids = [bin['bin_id'] for bin in full_bins]
        
        optimized_route = WasteCollection.optimize_routes(bin_ids)
        
        return jsonify({
            'optimized_route': optimized_route,
            'total_bins': len(optimized_route),
            'estimated_time': len(optimized_route) * 5,  # 5 minutes per bin
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to optimize routes', 'error': str(e)}), 500

@waste_bp.route('/analytics/efficiency', methods=['GET'])
@permission_required('waste.read')
def get_collection_efficiency(current_user):
    """Get waste collection efficiency metrics."""
    try:
        efficiency = WasteAnalytics.get_collection_efficiency()
        
        return jsonify({
            'efficiency_metrics': efficiency,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get efficiency metrics', 'error': str(e)}), 500

@waste_bp.route('/analytics/generation-trends', methods=['GET'])
@permission_required('waste.read')
def get_generation_trends(current_user):
    """Get waste generation trends."""
    try:
        days = int(request.args.get('days', 30))
        trends = WasteAnalytics.get_waste_generation_trends(days)
        
        return jsonify({
            'generation_trends': trends,
            'period_days': days,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to get generation trends', 'error': str(e)}), 500

@waste_bp.route('/reports/daily', methods=['GET'])
@permission_required('waste.read')
def get_daily_report(current_user):
    """Get daily waste management report."""
    try:
        today = datetime.now().date()
        
        # Get today's collections
        today_collections = WasteCollection.get_today_collections()
        completed_collections = [c for c in today_collections if c['status'] == 'completed']
        
        # Get bin statistics
        bin_stats = WasteBin.get_bin_statistics()
        full_bins = WasteBin.get_full_bins(threshold=80)
        
        report = {
            'date': today.isoformat(),
            'collections': {
                'scheduled': len(today_collections),
                'completed': len(completed_collections),
                'completion_rate': (len(completed_collections) / len(today_collections) * 100) if today_collections else 0
            },
            'bins': {
                'total': sum(stat['total_bins'] for stat in bin_stats),
                'full': len(full_bins),
                'types': bin_stats
            },
            'alerts': {
                'overflowing_bins': len([bin for bin in full_bins if bin['current_level'] >= 95]),
                'maintenance_needed': 0  # Placeholder
            }
        }
        
        return jsonify(report), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to generate daily report', 'error': str(e)}), 500

# Helper functions
def format_bin_data(data):
    """Format bin data for API response."""
    return {
        'id': str(data.get('_id', '')),
        'bin_id': data.get('bin_id'),
        'location': data.get('location'),
        'bin_type': data.get('bin_type'),
        'capacity': data.get('capacity'),
        'current_level': data.get('current_level'),
        'last_emptied': data.get('last_emptied').isoformat() if isinstance(data.get('last_emptied'), datetime) else data.get('last_emptied'),
        'status': data.get('status'),
        'created_at': data.get('created_at').isoformat() if isinstance(data.get('created_at'), datetime) else data.get('created_at')
    }

def format_collection_data(data):
    """Format collection data for API response."""
    return {
        'id': str(data.get('_id', '')),
        'route_id': data.get('route_id'),
        'route_name': data.get('route_name'),
        'assigned_vehicle': data.get('assigned_vehicle'),
        'assigned_crew': data.get('assigned_crew'),
        'scheduled_time': data.get('scheduled_time').isoformat() if isinstance(data.get('scheduled_time'), datetime) else data.get('scheduled_time'),
        'bin_ids': data.get('bin_ids'),
        'status': data.get('status'),
        'started_at': data.get('started_at').isoformat() if data.get('started_at') and isinstance(data.get('started_at'), datetime) else data.get('started_at'),
        'completed_at': data.get('completed_at').isoformat() if data.get('completed_at') and isinstance(data.get('completed_at'), datetime) else data.get('completed_at')
    }
