from datetime import datetime
from bson import ObjectId
from app import mongo

class WasteBin:
    """Waste bin monitoring model."""
    
    def __init__(self, bin_id, location, bin_type, capacity, current_level=0, 
                 last_emptied=None, status='active'):
        self.bin_id = bin_id
        self.location = location  # {'lat': float, 'lng': float, 'address': str}
        self.bin_type = bin_type  # general, recyclable, organic, hazardous
        self.capacity = capacity  # in liters
        self.current_level = current_level  # percentage (0-100)
        self.last_emptied = last_emptied or datetime.utcnow()
        self.status = status  # active, maintenance, out_of_service
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        """Save waste bin to database."""
        bin_data = {
            'bin_id': self.bin_id,
            'location': self.location,
            'bin_type': self.bin_type,
            'capacity': self.capacity,
            'current_level': self.current_level,
            'last_emptied': self.last_emptied,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        result = mongo.db.waste_bins.insert_one(bin_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update_level(bin_id, level):
        """Update waste bin level."""
        mongo.db.waste_bins.update_one(
            {'bin_id': bin_id},
            {
                '$set': {
                    'current_level': level,
                    'updated_at': datetime.utcnow()
                }
            }
        )
    
    @staticmethod
    def empty_bin(bin_id):
        """Mark bin as emptied."""
        mongo.db.waste_bins.update_one(
            {'bin_id': bin_id},
            {
                '$set': {
                    'current_level': 0,
                    'last_emptied': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            }
        )
    
    @staticmethod
    def get_all_bins():
        """Get all waste bins."""
        return list(mongo.db.waste_bins.find())
    
    @staticmethod
    def get_full_bins(threshold=80):
        """Get bins that are above threshold level."""
        return list(mongo.db.waste_bins.find({'current_level': {'$gte': threshold}}))
    
    @staticmethod
    def get_bin_statistics():
        """Get waste bin statistics."""
        pipeline = [
            {
                '$group': {
                    '_id': '$bin_type',
                    'total_bins': {'$sum': 1},
                    'avg_level': {'$avg': '$current_level'},
                    'full_bins': {
                        '$sum': {
                            '$cond': [{'$gte': ['$current_level', 80]}, 1, 0]
                        }
                    }
                }
            }
        ]
        return list(mongo.db.waste_bins.aggregate(pipeline))

class WasteCollection:
    """Waste collection route and schedule model."""
    
    def __init__(self, route_id, route_name, assigned_vehicle, assigned_crew, 
                 scheduled_time, bin_ids, status='scheduled'):
        self.route_id = route_id
        self.route_name = route_name
        self.assigned_vehicle = assigned_vehicle
        self.assigned_crew = assigned_crew  # list of crew member IDs
        self.scheduled_time = scheduled_time
        self.bin_ids = bin_ids  # list of bin IDs in route
        self.status = status  # scheduled, in_progress, completed, cancelled
        self.started_at = None
        self.completed_at = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        """Save collection route to database."""
        collection_data = {
            'route_id': self.route_id,
            'route_name': self.route_name,
            'assigned_vehicle': self.assigned_vehicle,
            'assigned_crew': self.assigned_crew,
            'scheduled_time': self.scheduled_time,
            'bin_ids': self.bin_ids,
            'status': self.status,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        result = mongo.db.waste_collections.insert_one(collection_data)
        return str(result.inserted_id)
    
    @staticmethod
    def start_collection(collection_id):
        """Start a collection route."""
        mongo.db.waste_collections.update_one(
            {'_id': ObjectId(collection_id)},
            {
                '$set': {
                    'status': 'in_progress',
                    'started_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            }
        )
    
    @staticmethod
    def complete_collection(collection_id):
        """Complete a collection route."""
        mongo.db.waste_collections.update_one(
            {'_id': ObjectId(collection_id)},
            {
                '$set': {
                    'status': 'completed',
                    'completed_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            }
        )
    
    @staticmethod
    def get_today_collections():
        """Get today's collection schedules."""
        from datetime import date
        today = datetime.combine(date.today(), datetime.min.time())
        tomorrow = datetime.combine(date.today(), datetime.max.time())
        
        return list(mongo.db.waste_collections.find({
            'scheduled_time': {'$gte': today, '$lte': tomorrow}
        }))
    
    @staticmethod
    def optimize_routes(bin_ids):
        """Optimize collection routes based on bin locations and levels."""
        # Get bin data
        bins = list(mongo.db.waste_bins.find({'bin_id': {'$in': bin_ids}}))
        
        # Simple optimization: group by proximity and priority (high level bins first)
        high_priority = [bin for bin in bins if bin['current_level'] >= 80]
        medium_priority = [bin for bin in bins if 50 <= bin['current_level'] < 80]
        low_priority = [bin for bin in bins if bin['current_level'] < 50]
        
        # Sort by location (simplified - in real implementation, use proper routing algorithm)
        optimized_route = high_priority + medium_priority + low_priority
        
        return [bin['bin_id'] for bin in optimized_route]

class WasteAnalytics:
    """Waste management analytics."""
    
    @staticmethod
    def get_collection_efficiency():
        """Calculate collection efficiency metrics."""
        pipeline = [
            {
                '$match': {
                    'status': 'completed',
                    'completed_at': {'$exists': True},
                    'started_at': {'$exists': True}
                }
            },
            {
                '$project': {
                    'duration': {
                        '$subtract': ['$completed_at', '$started_at']
                    },
                    'bins_collected': {'$size': '$bin_ids'}
                }
            },
            {
                '$group': {
                    '_id': None,
                    'avg_duration': {'$avg': '$duration'},
                    'avg_bins_per_route': {'$avg': '$bins_collected'},
                    'total_collections': {'$sum': 1}
                }
            }
        ]
        result = list(mongo.db.waste_collections.aggregate(pipeline))
        return result[0] if result else {}
    
    @staticmethod
    def get_waste_generation_trends(days=30):
        """Get waste generation trends."""
        from datetime import timedelta
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {'$match': {'updated_at': {'$gte': start_date}}},
            {
                '$group': {
                    '_id': {
                        'year': {'$year': '$updated_at'},
                        'month': {'$month': '$updated_at'},
                        'day': {'$dayOfMonth': '$updated_at'},
                        'bin_type': '$bin_type'
                    },
                    'avg_level': {'$avg': '$current_level'},
                    'max_level': {'$max': '$current_level'}
                }
            },
            {'$sort': {'_id': 1}}
        ]
        return list(mongo.db.waste_bins.aggregate(pipeline))
