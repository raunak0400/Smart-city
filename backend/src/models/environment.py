from datetime import datetime
from bson import ObjectId
from app import mongo

class EnvironmentData:
    """Environmental monitoring data model."""
    
    def __init__(self, sensor_id, location, air_quality_index, pm25, pm10, 
                 co2_level, noise_level, temperature, humidity, 
                 weather_condition='clear'):
        self.sensor_id = sensor_id
        self.location = location  # {'lat': float, 'lng': float, 'address': str}
        self.air_quality_index = air_quality_index  # 0-500 scale
        self.pm25 = pm25  # PM2.5 concentration (μg/m³)
        self.pm10 = pm10  # PM10 concentration (μg/m³)
        self.co2_level = co2_level  # CO2 concentration (ppm)
        self.noise_level = noise_level  # decibels
        self.temperature = temperature  # Celsius
        self.humidity = humidity  # percentage
        self.weather_condition = weather_condition
        self.timestamp = datetime.utcnow()
        self.created_at = datetime.utcnow()
    
    def save(self):
        """Save environment data to database."""
        env_data = {
            'sensor_id': self.sensor_id,
            'location': self.location,
            'air_quality_index': self.air_quality_index,
            'pm25': self.pm25,
            'pm10': self.pm10,
            'co2_level': self.co2_level,
            'noise_level': self.noise_level,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'weather_condition': self.weather_condition,
            'timestamp': self.timestamp,
            'created_at': self.created_at
        }
        result = mongo.db.environment_data.insert_one(env_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_latest_data(sensor_id=None, limit=100):
        """Get latest environmental data."""
        query = {}
        if sensor_id:
            query['sensor_id'] = sensor_id
        
        cursor = mongo.db.environment_data.find(query).sort('timestamp', -1).limit(limit)
        return list(cursor)
    
    @staticmethod
    def get_air_quality_summary():
        """Get air quality summary by zones."""
        pipeline = [
            {
                '$group': {
                    '_id': '$sensor_id',
                    'location': {'$first': '$location'},
                    'avg_aqi': {'$avg': '$air_quality_index'},
                    'avg_pm25': {'$avg': '$pm25'},
                    'avg_pm10': {'$avg': '$pm10'},
                    'avg_co2': {'$avg': '$co2_level'},
                    'latest_reading': {'$max': '$timestamp'}
                }
            }
        ]
        return list(mongo.db.environment_data.aggregate(pipeline))
    
    @staticmethod
    def get_pollution_trends(days=7):
        """Get pollution trends over specified days."""
        from datetime import timedelta
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {'$match': {'timestamp': {'$gte': start_date}}},
            {
                '$group': {
                    '_id': {
                        'year': {'$year': '$timestamp'},
                        'month': {'$month': '$timestamp'},
                        'day': {'$dayOfMonth': '$timestamp'}
                    },
                    'avg_aqi': {'$avg': '$air_quality_index'},
                    'avg_pm25': {'$avg': '$pm25'},
                    'avg_pm10': {'$avg': '$pm10'},
                    'avg_co2': {'$avg': '$co2_level'},
                    'avg_noise': {'$avg': '$noise_level'}
                }
            },
            {'$sort': {'_id': 1}}
        ]
        return list(mongo.db.environment_data.aggregate(pipeline))
    
    @staticmethod
    def check_pollution_alerts():
        """Check for pollution level alerts."""
        alerts = []
        
        # Get latest readings from all sensors
        latest_readings = mongo.db.environment_data.aggregate([
            {'$sort': {'timestamp': -1}},
            {
                '$group': {
                    '_id': '$sensor_id',
                    'latest_data': {'$first': '$$ROOT'}
                }
            }
        ])
        
        for reading in latest_readings:
            data = reading['latest_data']
            
            # Check AQI thresholds
            if data['air_quality_index'] > 300:
                alerts.append({
                    'type': 'air_quality',
                    'severity': 'critical',
                    'message': f"Hazardous air quality detected at {data['location']['address']}",
                    'sensor_id': data['sensor_id'],
                    'value': data['air_quality_index'],
                    'timestamp': data['timestamp']
                })
            elif data['air_quality_index'] > 200:
                alerts.append({
                    'type': 'air_quality',
                    'severity': 'high',
                    'message': f"Very unhealthy air quality at {data['location']['address']}",
                    'sensor_id': data['sensor_id'],
                    'value': data['air_quality_index'],
                    'timestamp': data['timestamp']
                })
            
            # Check noise level thresholds
            if data['noise_level'] > 85:
                alerts.append({
                    'type': 'noise',
                    'severity': 'high',
                    'message': f"Excessive noise level at {data['location']['address']}",
                    'sensor_id': data['sensor_id'],
                    'value': data['noise_level'],
                    'timestamp': data['timestamp']
                })
        
        return alerts

class EnvironmentAlert:
    """Environmental alert model."""
    
    def __init__(self, alert_type, severity, message, sensor_id, threshold_value, 
                 current_value, status='active'):
        self.alert_type = alert_type  # air_quality, noise, temperature
        self.severity = severity  # low, medium, high, critical
        self.message = message
        self.sensor_id = sensor_id
        self.threshold_value = threshold_value
        self.current_value = current_value
        self.status = status  # active, acknowledged, resolved
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.acknowledged_by = None
        self.resolved_at = None
    
    def save(self):
        """Save alert to database."""
        alert_data = {
            'alert_type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'sensor_id': self.sensor_id,
            'threshold_value': self.threshold_value,
            'current_value': self.current_value,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'acknowledged_by': self.acknowledged_by,
            'resolved_at': self.resolved_at
        }
        result = mongo.db.environment_alerts.insert_one(alert_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_active_alerts():
        """Get all active environmental alerts."""
        return list(mongo.db.environment_alerts.find({'status': 'active'}))
    
    @staticmethod
    def acknowledge_alert(alert_id, user_id):
        """Acknowledge an alert."""
        mongo.db.environment_alerts.update_one(
            {'_id': ObjectId(alert_id)},
            {
                '$set': {
                    'status': 'acknowledged',
                    'acknowledged_by': user_id,
                    'updated_at': datetime.utcnow()
                }
            }
        )
