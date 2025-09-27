# Smart City Management Platform - Backend

A production-ready Flask backend for the Smart City Management Platform with comprehensive city infrastructure monitoring and management capabilities.

## Features

### 🏗️ Core Infrastructure
- **Flask Application Factory Pattern** with modular design
- **JWT Authentication** with role-based access control
- **MongoDB Integration** with optimized indexes
- **Memory-based Rate Limiting** for API protection
- **WebSocket Support** for real-time updates
- **RESTful API** with comprehensive endpoints

### 🚦 Traffic Management
- Real-time traffic flow monitoring
- Congestion level tracking
- Incident reporting and management
- Signal timing optimization
- Route optimization for emergency vehicles
- Peak hours analysis and predictions

### 🌍 Environmental Monitoring
- Air quality index tracking (PM2.5, PM10, CO2)
- Noise level monitoring
- Temperature and humidity sensors
- Pollution trend analysis
- Environmental alerts and thresholds
- Health impact assessments

### 🗑️ Waste Management
- Smart bin level monitoring
- Collection route optimization
- Waste generation analytics
- Recycling rate tracking
- Cost analysis and efficiency metrics
- Automated collection scheduling

### ⚡ Energy Management
- Grid load monitoring and balancing
- Renewable energy tracking
- Consumption pattern analysis
- Energy efficiency recommendations
- Carbon footprint calculations
- Peak demand forecasting

### 🚨 Emergency Response
- Incident management system
- Emergency unit dispatch
- Response time tracking
- Public alert broadcasting
- Resource allocation optimization
- Emergency response planning

### 📊 Analytics & Reporting
- Real-time dashboards
- Predictive analytics
- KPI monitoring
- Comprehensive reporting
- Performance optimization
- Data visualization support

## Architecture

```
backend/
├── app.py                 # Application factory
├── config.py             # Configuration management
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
├── setup.py             # Setup script
├── gunicorn.conf.py     # Production server config
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Multi-service deployment
├── nginx.conf           # Reverse proxy config
├── mongo-init.js        # Database initialization
├── src/
│   ├── models/          # Data models
│   │   ├── user.py      # User authentication
│   │   ├── traffic.py   # Traffic management
│   │   ├── environment.py # Environmental data
│   │   ├── waste.py     # Waste management
│   │   └── energy.py    # Energy systems
│   ├── routes/          # API endpoints
│   │   ├── auth.py      # Authentication routes
│   │   ├── dashboard.py # Dashboard data
│   │   ├── traffic.py   # Traffic endpoints
│   │   ├── environment.py # Environment endpoints
│   │   ├── waste.py     # Waste endpoints
│   │   ├── energy.py    # Energy endpoints
│   │   ├── emergency.py # Emergency endpoints
│   │   ├── analytics.py # Analytics endpoints
│   │   └── alerts.py    # Alert management
│   ├── middleware/      # Request processing
│   │   ├── auth.py      # Authentication middleware
│   │   └── validation.py # Input validation
│   └── utils/           # Utility functions
│       ├── error_handlers.py # Error handling
│       ├── jwt_handlers.py   # JWT management
│       ├── helpers.py        # Helper functions
│       └── websocket_handlers.py # Real-time communication
└── logs/               # Application logs
```

## Quick Start

### Prerequisites
- Python 3.11+
- MongoDB 6.0+
- Node.js 16+ (for frontend, coming next)

### Installation

1. **Clone and setup backend:**
   ```bash
   cd backend
   python setup.py
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the backend:**
   ```bash
   # Simple startup (recommended)
   python start.py
   
   # Or manual startup
   python run.py
   
   # Production with Docker
   docker-compose up -d
   ```

### Default Admin Account
- **Email:** admin@smartcity.com
- **Password:** admin123
- **Role:** Administrator

## API Documentation

### Authentication Endpoints
```
POST /api/auth/login          # User login
POST /api/auth/register       # User registration (admin only)
POST /api/auth/refresh        # Refresh token
GET  /api/auth/profile        # Get user profile
PUT  /api/auth/profile        # Update profile
POST /api/auth/change-password # Change password
```

### Dashboard Endpoints
```
GET /api/dashboard/overview        # System overview
GET /api/dashboard/real-time-data  # Real-time metrics
GET /api/dashboard/alerts/summary  # Active alerts
GET /api/dashboard/statistics/weekly # Weekly statistics
```

### Traffic Management
```
GET  /api/traffic/data             # Traffic data
POST /api/traffic/data             # Add traffic data
GET  /api/traffic/incidents        # Traffic incidents
POST /api/traffic/incidents        # Report incident
GET  /api/traffic/optimization/signals # Signal optimization
POST /api/traffic/optimization/routes  # Route optimization
```

### Environmental Monitoring
```
GET  /api/environment/data         # Environmental data
POST /api/environment/data         # Add sensor data
GET  /api/environment/air-quality/summary # Air quality summary
GET  /api/environment/pollution/trends    # Pollution trends
GET  /api/environment/alerts       # Environmental alerts
```

### Waste Management
```
GET  /api/waste/bins              # Waste bins status
POST /api/waste/bins              # Add new bin
PUT  /api/waste/bins/:id/update-level # Update bin level
GET  /api/waste/collections       # Collection schedules
POST /api/waste/collections       # Schedule collection
POST /api/waste/optimization/routes # Optimize routes
```

### Energy Management
```
GET  /api/energy/grids            # Energy grid status
POST /api/energy/grids            # Add grid data
GET  /api/energy/consumption      # Energy consumption
GET  /api/energy/renewable        # Renewable energy data
GET  /api/energy/optimization/load-balancing # Load optimization
```

### Emergency Response
```
GET  /api/emergency/incidents     # Emergency incidents
POST /api/emergency/incidents     # Create incident
GET  /api/emergency/units         # Emergency units
POST /api/emergency/units/:id/dispatch # Dispatch unit
POST /api/emergency/alerts/broadcast   # Broadcast alert
```

### Analytics & Reports
```
GET /api/analytics/overview       # Analytics overview
GET /api/analytics/traffic/patterns # Traffic patterns
GET /api/analytics/predictive/traffic # Traffic predictions
GET /api/analytics/kpi/dashboard  # KPI dashboard
GET /api/analytics/reports/comprehensive # Comprehensive reports
```

## WebSocket Events

### Client Events
```javascript
// Connection
socket.emit('join_room', { room: 'traffic_monitoring' });
socket.emit('subscribe_alerts', { 
  severity_levels: ['high', 'critical'],
  modules: ['traffic', 'emergency'] 
});

// Real-time data requests
socket.emit('request_real_time_data', { data_type: 'traffic' });
```

### Server Events
```javascript
// Real-time updates
socket.on('traffic_update', (data) => { /* Handle traffic update */ });
socket.on('environment_alert', (alert) => { /* Handle alert */ });
socket.on('emergency_alert', (incident) => { /* Handle emergency */ });
socket.on('system_update', (update) => { /* Handle system update */ });
```

## Security Features

- **JWT Authentication** with refresh tokens
- **Role-based Access Control** (RBAC)
- **Rate Limiting** on API endpoints
- **Input Validation** with Marshmallow schemas
- **CORS Protection** with configurable origins
- **Password Hashing** with bcrypt
- **SQL Injection Prevention** with parameterized queries
- **XSS Protection** with content security policies

## Production Deployment

### Docker Deployment
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Scale backend instances
docker-compose up -d --scale backend=3
```

### Manual Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn --config gunicorn.conf.py run:app

# Or with uWSGI
uwsgi --ini uwsgi.ini
```

### Environment Variables
```bash
# Database
MONGO_URI=mongodb://localhost:27017/smart_city_db
REDIS_URL=redis://localhost:6379/0

# Security
JWT_SECRET_KEY=your-super-secret-jwt-key
SECRET_KEY=your-flask-secret-key

# Email (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# External APIs (optional)
WEATHER_API_KEY=your-weather-api-key
MAPS_API_KEY=your-google-maps-api-key
```

## Monitoring & Logging

### Health Checks
```bash
# Application health
curl http://localhost:5000/api/health

# Database connectivity
curl http://localhost:5000/api/health | jq '.services.database'
```

### Logging
- **Application logs:** `logs/smart_city.log`
- **Access logs:** Nginx access logs
- **Error logs:** Nginx error logs
- **Container logs:** `docker-compose logs`

### Metrics
- Response times and throughput
- Database query performance
- Memory and CPU usage
- Active WebSocket connections
- API endpoint usage statistics

## Testing

### Unit Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_auth.py
```

### API Testing
```bash
# Test with curl
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@smartcity.com", "password": "admin123"}'

# Test with httpie
http POST localhost:5000/api/auth/login email=admin@smartcity.com password=admin123
```

## Performance Optimization

### Database Optimization
- Indexed collections for fast queries
- Aggregation pipelines for complex analytics
- Connection pooling for concurrent requests
- Query optimization with explain plans

### Caching Strategy
- Redis for session storage
- API response caching
- Database query result caching
- Static asset caching with CDN

### Scaling Considerations
- Horizontal scaling with load balancers
- Database sharding for large datasets
- Microservices architecture for specific modules
- Message queues for background processing

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   ```bash
   # Check MongoDB status
   sudo systemctl status mongod
   
   # Start MongoDB
   sudo systemctl start mongod
   ```

2. **Redis Connection Failed**
   ```bash
   # Check Redis status
   sudo systemctl status redis
   
   # Start Redis
   sudo systemctl start redis
   ```

3. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   
   # Kill process
   kill -9 <PID>
   ```

4. **Permission Denied**
   ```bash
   # Fix file permissions
   chmod +x run.py setup.py
   
   # Fix directory permissions
   chmod -R 755 logs/
   ```

### Debug Mode
```bash
# Enable debug mode
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API examples
- Join our community discussions
