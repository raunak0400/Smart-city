from datetime import datetime
from bson import ObjectId
from app import mongo

class TrafficData:
    """Traffic monitoring and management data model."""
    
    def __init__(self, intersection_id, location, traffic_flow, congestion_level, 
                 signal_timing=None, vehicle_count=None, average_speed=None, 
                 incident_reported=False, weather_condition='clear'):
        self.intersection_id = intersection_id
        self.location = location  # {'lat': float, 'lng': float, 'address': str}
        self.traffic_flow = traffic_flow  # vehicles per hour
        self.congestion_level = congestion_level  # low, medium, high, critical
        self.signal_timing = signal_timing or {'red': 30, 'yellow': 5, 'green': 45}
        self.vehicle_count = vehicle_count or 0
        self.average_speed = average_speed or 0.0  # km/h
        self.incident_reported = incident_reported
        self.weather_condition = weather_condition
        self.timestamp = datetime.utcnow()
        self.created_at = datetime.utcnow()
    
    def save(self):
        """Save traffic data to database."""
        traffic_data = {
            'intersection_id': self.intersection_id,
            'location': self.location,
            'traffic_flow': self.traffic_flow,
            'congestion_level': self.congestion_level,
            'signal_timing': self.signal_timing,
            'vehicle_count': self.vehicle_count,
            'average_speed': self.average_speed,
            'incident_reported': self.incident_reported,
            'weather_condition': self.weather_condition,
            'timestamp': self.timestamp,
            'created_at': self.created_at
        }
        result = mongo.db.traffic_data.insert_one(traffic_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_latest_data(intersection_id=None, limit=100):
        """Get latest traffic data."""
        query = {}
        if intersection_id:
            query['intersection_id'] = intersection_id
        
        cursor = mongo.db.traffic_data.find(query).sort('timestamp', -1).limit(limit)
        return list(cursor)
    
    @staticmethod
    def get_congestion_summary():
        """Get traffic congestion summary."""
        pipeline = [
            {
                '$group': {
                    '_id': '$congestion_level',
                    'count': {'$sum': 1},
                    'avg_flow': {'$avg': '$traffic_flow'},
                    'avg_speed': {'$avg': '$average_speed'}
                }
            }
        ]
        return list(mongo.db.traffic_data.aggregate(pipeline))
    
    @staticmethod
    def get_peak_hours_analysis():
        """Analyze peak traffic hours."""
        pipeline = [
            {
                '$group': {
                    '_id': {'$hour': '$timestamp'},
                    'avg_flow': {'$avg': '$traffic_flow'},
                    'avg_congestion': {
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
            {'$sort': {'_id': 1}}
        ]
        return list(mongo.db.traffic_data.aggregate(pipeline))

class TrafficIncident:
    """Traffic incident model."""
    
    def __init__(self, location, incident_type, severity, description, 
                 reported_by, status='active'):
        self.location = location
        self.incident_type = incident_type  # accident, roadwork, weather, other
        self.severity = severity  # low, medium, high, critical
        self.description = description
        self.reported_by = reported_by
        self.status = status  # active, resolved, investigating
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.resolved_at = None
    
    def save(self):
        """Save incident to database."""
        incident_data = {
            'location': self.location,
            'incident_type': self.incident_type,
            'severity': self.severity,
            'description': self.description,
            'reported_by': self.reported_by,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'resolved_at': self.resolved_at
        }
        result = mongo.db.traffic_incidents.insert_one(incident_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_active_incidents():
        """Get all active incidents."""
        return list(mongo.db.traffic_incidents.find({'status': 'active'}))
    
    @staticmethod
    def resolve_incident(incident_id):
        """Mark incident as resolved."""
        mongo.db.traffic_incidents.update_one(
            {'_id': ObjectId(incident_id)},
            {
                '$set': {
                    'status': 'resolved',
                    'resolved_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            }
        )
