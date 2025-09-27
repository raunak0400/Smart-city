from datetime import datetime
from bson import ObjectId
from app import mongo

class EnergyGrid:
    """Energy grid monitoring and management model."""
    
    def __init__(self, grid_id, grid_name, location, capacity, current_load, 
                 voltage, frequency, status='operational'):
        self.grid_id = grid_id
        self.grid_name = grid_name
        self.location = location  # {'lat': float, 'lng': float, 'address': str}
        self.capacity = capacity  # in MW
        self.current_load = current_load  # in MW
        self.voltage = voltage  # in kV
        self.frequency = frequency  # in Hz
        self.status = status  # operational, maintenance, fault, offline
        self.timestamp = datetime.utcnow()
        self.created_at = datetime.utcnow()
    
    def save(self):
        """Save energy grid data to database."""
        grid_data = {
            'grid_id': self.grid_id,
            'grid_name': self.grid_name,
            'location': self.location,
            'capacity': self.capacity,
            'current_load': self.current_load,
            'voltage': self.voltage,
            'frequency': self.frequency,
            'status': self.status,
            'timestamp': self.timestamp,
            'created_at': self.created_at
        }
        result = mongo.db.energy_grids.insert_one(grid_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_latest_data(grid_id=None):
        """Get latest energy grid data."""
        if grid_id:
            return mongo.db.energy_grids.find_one(
                {'grid_id': grid_id}, 
                sort=[('timestamp', -1)]
            )
        else:
            pipeline = [
                {'$sort': {'timestamp': -1}},
                {
                    '$group': {
                        '_id': '$grid_id',
                        'latest_data': {'$first': '$$ROOT'}
                    }
                }
            ]
            return list(mongo.db.energy_grids.aggregate(pipeline))
    
    @staticmethod
    def get_load_distribution():
        """Get current load distribution across grids."""
        pipeline = [
            {'$sort': {'timestamp': -1}},
            {
                '$group': {
                    '_id': '$grid_id',
                    'grid_name': {'$first': '$grid_name'},
                    'capacity': {'$first': '$capacity'},
                    'current_load': {'$first': '$current_load'},
                    'load_percentage': {
                        '$first': {
                            '$multiply': [
                                {'$divide': ['$current_load', '$capacity']}, 
                                100
                            ]
                        }
                    },
                    'status': {'$first': '$status'}
                }
            }
        ]
        return list(mongo.db.energy_grids.aggregate(pipeline))
    
    @staticmethod
    def check_overload_alerts():
        """Check for grid overload conditions."""
        alerts = []
        latest_data = EnergyGrid.get_latest_data()
        
        for grid in latest_data:
            data = grid['latest_data']
            load_percentage = (data['current_load'] / data['capacity']) * 100
            
            if load_percentage > 95:
                alerts.append({
                    'type': 'overload',
                    'severity': 'critical',
                    'message': f"Critical overload in {data['grid_name']}",
                    'grid_id': data['grid_id'],
                    'load_percentage': load_percentage,
                    'timestamp': data['timestamp']
                })
            elif load_percentage > 85:
                alerts.append({
                    'type': 'high_load',
                    'severity': 'high',
                    'message': f"High load in {data['grid_name']}",
                    'grid_id': data['grid_id'],
                    'load_percentage': load_percentage,
                    'timestamp': data['timestamp']
                })
        
        return alerts

class EnergyConsumption:
    """Energy consumption tracking model."""
    
    def __init__(self, meter_id, location, consumer_type, consumption, 
                 peak_demand, cost, billing_period):
        self.meter_id = meter_id
        self.location = location
        self.consumer_type = consumer_type  # residential, commercial, industrial, public
        self.consumption = consumption  # kWh
        self.peak_demand = peak_demand  # kW
        self.cost = cost  # currency
        self.billing_period = billing_period  # {'start': date, 'end': date}
        self.timestamp = datetime.utcnow()
        self.created_at = datetime.utcnow()
    
    def save(self):
        """Save consumption data to database."""
        consumption_data = {
            'meter_id': self.meter_id,
            'location': self.location,
            'consumer_type': self.consumer_type,
            'consumption': self.consumption,
            'peak_demand': self.peak_demand,
            'cost': self.cost,
            'billing_period': self.billing_period,
            'timestamp': self.timestamp,
            'created_at': self.created_at
        }
        result = mongo.db.energy_consumption.insert_one(consumption_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_consumption_by_type():
        """Get consumption statistics by consumer type."""
        pipeline = [
            {
                '$group': {
                    '_id': '$consumer_type',
                    'total_consumption': {'$sum': '$consumption'},
                    'avg_consumption': {'$avg': '$consumption'},
                    'total_cost': {'$sum': '$cost'},
                    'consumer_count': {'$sum': 1}
                }
            }
        ]
        return list(mongo.db.energy_consumption.aggregate(pipeline))
    
    @staticmethod
    def get_peak_demand_analysis():
        """Analyze peak demand patterns."""
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'hour': {'$hour': '$timestamp'},
                        'consumer_type': '$consumer_type'
                    },
                    'avg_demand': {'$avg': '$peak_demand'},
                    'max_demand': {'$max': '$peak_demand'}
                }
            },
            {'$sort': {'_id.hour': 1}}
        ]
        return list(mongo.db.energy_consumption.aggregate(pipeline))

class RenewableEnergy:
    """Renewable energy sources tracking."""
    
    def __init__(self, source_id, source_type, location, capacity, 
                 current_generation, efficiency, weather_condition='clear'):
        self.source_id = source_id
        self.source_type = source_type  # solar, wind, hydro, biomass
        self.location = location
        self.capacity = capacity  # in MW
        self.current_generation = current_generation  # in MW
        self.efficiency = efficiency  # percentage
        self.weather_condition = weather_condition
        self.timestamp = datetime.utcnow()
        self.created_at = datetime.utcnow()
    
    def save(self):
        """Save renewable energy data to database."""
        renewable_data = {
            'source_id': self.source_id,
            'source_type': self.source_type,
            'location': self.location,
            'capacity': self.capacity,
            'current_generation': self.current_generation,
            'efficiency': self.efficiency,
            'weather_condition': self.weather_condition,
            'timestamp': self.timestamp,
            'created_at': self.created_at
        }
        result = mongo.db.renewable_energy.insert_one(renewable_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_renewable_summary():
        """Get renewable energy generation summary."""
        pipeline = [
            {'$sort': {'timestamp': -1}},
            {
                '$group': {
                    '_id': '$source_type',
                    'total_capacity': {'$sum': '$capacity'},
                    'total_generation': {'$sum': '$current_generation'},
                    'avg_efficiency': {'$avg': '$efficiency'},
                    'source_count': {'$sum': 1}
                }
            }
        ]
        return list(mongo.db.renewable_energy.aggregate(pipeline))
    
    @staticmethod
    def get_generation_forecast(source_type=None):
        """Get generation forecast based on weather conditions."""
        # Simplified forecast based on current efficiency trends
        query = {}
        if source_type:
            query['source_type'] = source_type
        
        pipeline = [
            {'$match': query},
            {'$sort': {'timestamp': -1}},
            {'$limit': 24},  # Last 24 hours
            {
                '$group': {
                    '_id': '$source_type',
                    'avg_efficiency': {'$avg': '$efficiency'},
                    'capacity': {'$first': '$capacity'},
                    'predicted_generation': {
                        '$multiply': ['$capacity', {'$divide': ['$avg_efficiency', 100]}]
                    }
                }
            }
        ]
        return list(mongo.db.renewable_energy.aggregate(pipeline))

class EnergyOptimization:
    """Energy optimization and load balancing."""
    
    @staticmethod
    def optimize_load_distribution():
        """Optimize load distribution across grids."""
        grids = EnergyGrid.get_latest_data()
        total_capacity = sum(grid['latest_data']['capacity'] for grid in grids)
        total_load = sum(grid['latest_data']['current_load'] for grid in grids)
        
        optimization_plan = []
        
        for grid in grids:
            data = grid['latest_data']
            current_percentage = (data['current_load'] / data['capacity']) * 100
            optimal_percentage = (total_load / total_capacity) * 100
            
            if current_percentage > optimal_percentage + 10:
                optimization_plan.append({
                    'grid_id': data['grid_id'],
                    'action': 'reduce_load',
                    'current_load': data['current_load'],
                    'recommended_load': data['capacity'] * (optimal_percentage / 100),
                    'priority': 'high' if current_percentage > 90 else 'medium'
                })
            elif current_percentage < optimal_percentage - 10:
                optimization_plan.append({
                    'grid_id': data['grid_id'],
                    'action': 'increase_load',
                    'current_load': data['current_load'],
                    'recommended_load': data['capacity'] * (optimal_percentage / 100),
                    'priority': 'low'
                })
        
        return optimization_plan
    
    @staticmethod
    def get_energy_efficiency_recommendations():
        """Generate energy efficiency recommendations."""
        consumption_data = EnergyConsumption.get_consumption_by_type()
        renewable_data = RenewableEnergy.get_renewable_summary()
        
        recommendations = []
        
        # Analyze consumption patterns
        for consumer in consumption_data:
            if consumer['avg_consumption'] > 1000:  # High consumption threshold
                recommendations.append({
                    'type': 'consumption_reduction',
                    'target': consumer['_id'],
                    'message': f"High energy consumption detected in {consumer['_id']} sector",
                    'recommendation': "Implement energy-efficient technologies and practices",
                    'potential_savings': consumer['avg_consumption'] * 0.15  # 15% savings
                })
        
        # Renewable energy recommendations
        total_renewable = sum(source['total_generation'] for source in renewable_data)
        total_consumption = sum(consumer['total_consumption'] for consumer in consumption_data)
        
        if total_renewable < total_consumption * 0.3:  # Less than 30% renewable
            recommendations.append({
                'type': 'renewable_expansion',
                'message': "Low renewable energy contribution",
                'recommendation': "Increase renewable energy capacity",
                'target_percentage': 30,
                'current_percentage': (total_renewable / total_consumption) * 100
            })
        
        return recommendations
