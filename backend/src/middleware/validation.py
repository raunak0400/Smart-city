from functools import wraps
from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError

def validate_json(schema_class):
    """Decorator to validate JSON input using Marshmallow schema."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                if not request.is_json:
                    return jsonify({'message': 'Content-Type must be application/json'}), 400
                
                schema = schema_class()
                data = schema.load(request.get_json())
                return f(data, *args, **kwargs)
            except ValidationError as err:
                return jsonify({'message': 'Validation error', 'errors': err.messages}), 400
            except Exception as e:
                return jsonify({'message': 'Invalid JSON format'}), 400
        
        return decorated
    return decorator

# User Schemas
class UserRegistrationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 8)
    first_name = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    last_name = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)
    role = fields.Str(required=True, validate=lambda x: x in ['admin', 'traffic_officer', 'environment_officer', 'utility_officer', 'emergency_coordinator'])
    phone = fields.Str(required=False)
    department = fields.Str(required=False)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

# Traffic Schemas
class TrafficDataSchema(Schema):
    intersection_id = fields.Str(required=True)
    location = fields.Dict(required=True)
    traffic_flow = fields.Int(required=True, validate=lambda x: x >= 0)
    congestion_level = fields.Str(required=True, validate=lambda x: x in ['low', 'medium', 'high', 'critical'])
    signal_timing = fields.Dict(required=False)
    vehicle_count = fields.Int(required=False, validate=lambda x: x >= 0)
    average_speed = fields.Float(required=False, validate=lambda x: x >= 0)
    incident_reported = fields.Bool(required=False)
    weather_condition = fields.Str(required=False)

class TrafficIncidentSchema(Schema):
    location = fields.Dict(required=True)
    incident_type = fields.Str(required=True, validate=lambda x: x in ['accident', 'roadwork', 'weather', 'other'])
    severity = fields.Str(required=True, validate=lambda x: x in ['low', 'medium', 'high', 'critical'])
    description = fields.Str(required=True)
    reported_by = fields.Str(required=True)

# Environment Schemas
class EnvironmentDataSchema(Schema):
    sensor_id = fields.Str(required=True)
    location = fields.Dict(required=True)
    air_quality_index = fields.Int(required=True, validate=lambda x: 0 <= x <= 500)
    pm25 = fields.Float(required=True, validate=lambda x: x >= 0)
    pm10 = fields.Float(required=True, validate=lambda x: x >= 0)
    co2_level = fields.Float(required=True, validate=lambda x: x >= 0)
    noise_level = fields.Float(required=True, validate=lambda x: x >= 0)
    temperature = fields.Float(required=True)
    humidity = fields.Float(required=True, validate=lambda x: 0 <= x <= 100)
    weather_condition = fields.Str(required=False)

# Waste Management Schemas
class WasteBinSchema(Schema):
    bin_id = fields.Str(required=True)
    location = fields.Dict(required=True)
    bin_type = fields.Str(required=True, validate=lambda x: x in ['general', 'recyclable', 'organic', 'hazardous'])
    capacity = fields.Int(required=True, validate=lambda x: x > 0)
    current_level = fields.Int(required=False, validate=lambda x: 0 <= x <= 100)

class WasteCollectionSchema(Schema):
    route_id = fields.Str(required=True)
    route_name = fields.Str(required=True)
    assigned_vehicle = fields.Str(required=True)
    assigned_crew = fields.List(fields.Str(), required=True)
    scheduled_time = fields.DateTime(required=True)
    bin_ids = fields.List(fields.Str(), required=True)

# Energy Schemas
class EnergyGridSchema(Schema):
    grid_id = fields.Str(required=True)
    grid_name = fields.Str(required=True)
    location = fields.Dict(required=True)
    capacity = fields.Float(required=True, validate=lambda x: x > 0)
    current_load = fields.Float(required=True, validate=lambda x: x >= 0)
    voltage = fields.Float(required=True, validate=lambda x: x > 0)
    frequency = fields.Float(required=True, validate=lambda x: x > 0)
    status = fields.Str(required=False, validate=lambda x: x in ['operational', 'maintenance', 'fault', 'offline'])

class EnergyConsumptionSchema(Schema):
    meter_id = fields.Str(required=True)
    location = fields.Dict(required=True)
    consumer_type = fields.Str(required=True, validate=lambda x: x in ['residential', 'commercial', 'industrial', 'public'])
    consumption = fields.Float(required=True, validate=lambda x: x >= 0)
    peak_demand = fields.Float(required=True, validate=lambda x: x >= 0)
    cost = fields.Float(required=True, validate=lambda x: x >= 0)
    billing_period = fields.Dict(required=True)

class RenewableEnergySchema(Schema):
    source_id = fields.Str(required=True)
    source_type = fields.Str(required=True, validate=lambda x: x in ['solar', 'wind', 'hydro', 'biomass'])
    location = fields.Dict(required=True)
    capacity = fields.Float(required=True, validate=lambda x: x > 0)
    current_generation = fields.Float(required=True, validate=lambda x: x >= 0)
    efficiency = fields.Float(required=True, validate=lambda x: 0 <= x <= 100)
    weather_condition = fields.Str(required=False)

# Alert Schemas
class AlertSchema(Schema):
    alert_type = fields.Str(required=True)
    severity = fields.Str(required=True, validate=lambda x: x in ['low', 'medium', 'high', 'critical'])
    message = fields.Str(required=True)
    module = fields.Str(required=True, validate=lambda x: x in ['traffic', 'environment', 'waste', 'energy', 'emergency'])
    threshold_value = fields.Float(required=False)
    current_value = fields.Float(required=False)
