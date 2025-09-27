// MongoDB initialization script
// This script runs when the MongoDB container starts for the first time

// Switch to the smart_city_db database
db = db.getSiblingDB('smart_city_db');

// Create collections with indexes for better performance

// Users collection
db.createCollection('users');
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "role": 1 });
db.users.createIndex({ "is_active": 1 });

// Traffic data collection
db.createCollection('traffic_data');
db.traffic_data.createIndex({ "intersection_id": 1 });
db.traffic_data.createIndex({ "timestamp": -1 });
db.traffic_data.createIndex({ "congestion_level": 1 });
db.traffic_data.createIndex({ "location.lat": 1, "location.lng": 1 });

// Traffic incidents collection
db.createCollection('traffic_incidents');
db.traffic_incidents.createIndex({ "status": 1 });
db.traffic_incidents.createIndex({ "severity": 1 });
db.traffic_incidents.createIndex({ "created_at": -1 });
db.traffic_incidents.createIndex({ "location.lat": 1, "location.lng": 1 });

// Environment data collection
db.createCollection('environment_data');
db.environment_data.createIndex({ "sensor_id": 1 });
db.environment_data.createIndex({ "timestamp": -1 });
db.environment_data.createIndex({ "air_quality_index": 1 });
db.environment_data.createIndex({ "location.lat": 1, "location.lng": 1 });

// Environment alerts collection
db.createCollection('environment_alerts');
db.environment_alerts.createIndex({ "status": 1 });
db.environment_alerts.createIndex({ "severity": 1 });
db.environment_alerts.createIndex({ "sensor_id": 1 });
db.environment_alerts.createIndex({ "created_at": -1 });

// Waste bins collection
db.createCollection('waste_bins');
db.waste_bins.createIndex({ "bin_id": 1 }, { unique: true });
db.waste_bins.createIndex({ "bin_type": 1 });
db.waste_bins.createIndex({ "current_level": 1 });
db.waste_bins.createIndex({ "status": 1 });
db.waste_bins.createIndex({ "location.lat": 1, "location.lng": 1 });

// Waste collections collection
db.createCollection('waste_collections');
db.waste_collections.createIndex({ "route_id": 1 });
db.waste_collections.createIndex({ "status": 1 });
db.waste_collections.createIndex({ "scheduled_time": 1 });
db.waste_collections.createIndex({ "assigned_vehicle": 1 });

// Energy grids collection
db.createCollection('energy_grids');
db.energy_grids.createIndex({ "grid_id": 1 });
db.energy_grids.createIndex({ "timestamp": -1 });
db.energy_grids.createIndex({ "status": 1 });
db.energy_grids.createIndex({ "location.lat": 1, "location.lng": 1 });

// Energy consumption collection
db.createCollection('energy_consumption');
db.energy_consumption.createIndex({ "meter_id": 1 });
db.energy_consumption.createIndex({ "consumer_type": 1 });
db.energy_consumption.createIndex({ "timestamp": -1 });
db.energy_consumption.createIndex({ "billing_period.start": 1, "billing_period.end": 1 });

// Renewable energy collection
db.createCollection('renewable_energy');
db.renewable_energy.createIndex({ "source_id": 1 });
db.renewable_energy.createIndex({ "source_type": 1 });
db.renewable_energy.createIndex({ "timestamp": -1 });
db.renewable_energy.createIndex({ "location.lat": 1, "location.lng": 1 });

// Emergency incidents collection
db.createCollection('emergency_incidents');
db.emergency_incidents.createIndex({ "status": 1 });
db.emergency_incidents.createIndex({ "severity": 1 });
db.emergency_incidents.createIndex({ "incident_type": 1 });
db.emergency_incidents.createIndex({ "created_at": -1 });
db.emergency_incidents.createIndex({ "location.lat": 1, "location.lng": 1 });

// Emergency units collection
db.createCollection('emergency_units');
db.emergency_units.createIndex({ "unit_id": 1 }, { unique: true });
db.emergency_units.createIndex({ "unit_type": 1 });
db.emergency_units.createIndex({ "status": 1 });
db.emergency_units.createIndex({ "location.lat": 1, "location.lng": 1 });

// Emergency response plans collection
db.createCollection('emergency_response_plans');
db.emergency_response_plans.createIndex({ "incident_id": 1 });
db.emergency_response_plans.createIndex({ "status": 1 });
db.emergency_response_plans.createIndex({ "created_at": -1 });

// Emergency alerts collection
db.createCollection('emergency_alerts');
db.emergency_alerts.createIndex({ "alert_type": 1 });
db.emergency_alerts.createIndex({ "severity": 1 });
db.emergency_alerts.createIndex({ "created_at": -1 });
db.emergency_alerts.createIndex({ "expires_at": 1 });

// General alerts collection
db.createCollection('alerts');
db.alerts.createIndex({ "status": 1 });
db.alerts.createIndex({ "severity": 1 });
db.alerts.createIndex({ "module": 1 });
db.alerts.createIndex({ "alert_type": 1 });
db.alerts.createIndex({ "created_at": -1 });

// Alert rules collection
db.createCollection('alert_rules');
db.alert_rules.createIndex({ "module": 1 });
db.alert_rules.createIndex({ "enabled": 1 });
db.alert_rules.createIndex({ "created_at": -1 });

// Notification settings collection
db.createCollection('notification_settings');
db.notification_settings.createIndex({ "user_id": 1 }, { unique: true });

// Create default admin user
db.users.insertOne({
    email: "admin@smartcity.com",
    password_hash: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj3QJgusgqHG", // password: admin123
    first_name: "System",
    last_name: "Administrator",
    role: "admin",
    phone: "+1234567890",
    department: "IT",
    is_active: true,
    created_at: new Date(),
    updated_at: new Date(),
    last_login: null
});

// Create sample data for demonstration
// Sample traffic intersections
db.traffic_data.insertMany([
    {
        intersection_id: "INT_001",
        location: { lat: 40.7128, lng: -74.0060, address: "Times Square, NYC" },
        traffic_flow: 1250,
        congestion_level: "medium",
        signal_timing: { red: 30, yellow: 5, green: 45 },
        vehicle_count: 85,
        average_speed: 25.5,
        incident_reported: false,
        weather_condition: "clear",
        timestamp: new Date(),
        created_at: new Date()
    },
    {
        intersection_id: "INT_002",
        location: { lat: 40.7589, lng: -73.9851, address: "Central Park South, NYC" },
        traffic_flow: 890,
        congestion_level: "low",
        signal_timing: { red: 25, yellow: 5, green: 40 },
        vehicle_count: 45,
        average_speed: 35.2,
        incident_reported: false,
        weather_condition: "clear",
        timestamp: new Date(),
        created_at: new Date()
    }
]);

// Sample environment sensors
db.environment_data.insertMany([
    {
        sensor_id: "ENV_001",
        location: { lat: 40.7128, lng: -74.0060, address: "Downtown Monitoring Station" },
        air_quality_index: 85,
        pm25: 25.3,
        pm10: 45.7,
        co2_level: 410.5,
        noise_level: 65.2,
        temperature: 22.5,
        humidity: 68.0,
        weather_condition: "clear",
        timestamp: new Date(),
        created_at: new Date()
    },
    {
        sensor_id: "ENV_002",
        location: { lat: 40.7589, lng: -73.9851, address: "Park Area Monitoring Station" },
        air_quality_index: 72,
        pm25: 18.9,
        pm10: 32.1,
        co2_level: 395.2,
        noise_level: 52.8,
        temperature: 23.1,
        humidity: 65.5,
        weather_condition: "clear",
        timestamp: new Date(),
        created_at: new Date()
    }
]);

// Sample waste bins
db.waste_bins.insertMany([
    {
        bin_id: "BIN_001",
        location: { lat: 40.7128, lng: -74.0060, address: "Main Street & 1st Ave" },
        bin_type: "general",
        capacity: 240,
        current_level: 65,
        last_emptied: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
        status: "active",
        created_at: new Date(),
        updated_at: new Date()
    },
    {
        bin_id: "BIN_002",
        location: { lat: 40.7589, lng: -73.9851, address: "Park Avenue & 5th St" },
        bin_type: "recyclable",
        capacity: 240,
        current_level: 45,
        last_emptied: new Date(Date.now() - 12 * 60 * 60 * 1000), // 12 hours ago
        status: "active",
        created_at: new Date(),
        updated_at: new Date()
    }
]);

// Sample energy grids
db.energy_grids.insertMany([
    {
        grid_id: "GRID_001",
        grid_name: "Downtown Power Grid",
        location: { lat: 40.7128, lng: -74.0060, address: "Downtown Power Station" },
        capacity: 500.0,
        current_load: 387.5,
        voltage: 115.2,
        frequency: 60.0,
        status: "operational",
        timestamp: new Date(),
        created_at: new Date()
    },
    {
        grid_id: "GRID_002",
        grid_name: "Residential Area Grid",
        location: { lat: 40.7589, lng: -73.9851, address: "Residential Power Station" },
        capacity: 300.0,
        current_load: 245.8,
        voltage: 114.8,
        frequency: 59.9,
        status: "operational",
        timestamp: new Date(),
        created_at: new Date()
    }
]);

print("Smart City database initialized successfully with sample data!");
