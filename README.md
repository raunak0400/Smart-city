# Smart City Management Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-000000.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-47A248.svg)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Security](https://img.shields.io/badge/Security-Policy-red.svg)](./SECURITY.md)
[![Maintenance](https://img.shields.io/badge/Maintained-Yes-green.svg)](https://github.com/prathamupadhyay341/smart-city-management)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

A comprehensive digital solution for city administrators to monitor, analyze, and improve urban infrastructure and public services.

## Features

### 🏗️ **Core Platform**
- **Centralized Dashboard**: Real-time city operations monitoring with live KPIs
- **Role-Based Access Control**: Secure authentication with 5 user roles
- **Real-Time Alerts**: WebSocket-powered instant notifications
- **Predictive Analytics**: AI/ML insights for resource optimization
- **Multi-Module Architecture**: Integrated city management systems

### 🚦 **Traffic Management**
- Real-time traffic flow monitoring and congestion tracking
- Incident reporting and management system
- Signal timing optimization algorithms
- Route optimization for emergency vehicles
- Traffic pattern analysis and predictions

### 🌍 **Environmental Monitoring**
- Air quality index (AQI) tracking with PM2.5, PM10, NO2, O3
- Environmental sensor network management
- Pollution trend analysis and forecasting
- Automated environmental alerts and thresholds
- Climate impact assessments

### 🗑️ **Waste Management**
- Smart bin level monitoring with IoT sensors
- Collection route optimization algorithms
- Waste generation analytics and reporting
- Recycling rate tracking and optimization
- Cost analysis and efficiency metrics

### ⚡ **Energy Management**
- Grid load monitoring and balancing
- Renewable energy source tracking (solar, wind, hydro)
- Energy consumption pattern analysis
- Peak demand forecasting and management
- Carbon footprint calculations and reduction tracking

### 🚨 **Emergency Response**
- Incident management and coordination system
- Emergency unit dispatch and tracking
- Response time monitoring and optimization
- Public alert broadcasting system
- Resource allocation and planning tools

### 📊 **Analytics & Reporting**
- Comprehensive KPI dashboards with trend analysis
- Predictive analytics for all city systems
- Performance optimization recommendations
- Automated report generation (PDF/CSV export)
- Data visualization with interactive charts

## Architecture

- **Frontend**: React.js with Tailwind CSS and Bootstrap
- **Backend**: Flask with Python (Production-Ready)
- **Database**: MongoDB with optimized indexes
- **Authentication**: JWT-based with role management
- **Real-time**: WebSocket connections for live updates
- **Rate Limiting**: Memory-based API protection
- **Deployment**: Docker containerization with Nginx

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js (v16 or higher)
- MongoDB 6.0+
- Docker (optional, for containerized deployment)

### Quick Start

#### Option 1: Automated Setup (Recommended)
```bash
# Backend setup
cd backend
python setup.py

# Start services
python start.py
```

#### Option 2: Full Stack Deployment (Recommended)
```bash
# Deploy entire platform with Docker
python deploy-full-stack.py

# Or manual Docker commands
docker-compose up -d
```

#### Option 3: Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python run.py

# Frontend
cd frontend
npm install
node start.js
```

### Default Access
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Admin Login**: admin@smartcity.com / admin123
- **Health Check**: http://localhost:5000/api/health

## Project Structure

```
Smart-City-Management/
├── backend/                 # Flask backend (Production-Ready)
│   ├── src/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Helper functions
│   │   └── websocket/      # Real-time features
│   ├── config.py           # Configuration management
│   ├── app.py              # Application factory
│   ├── run.py              # Application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── setup.py            # Automated setup script
│   ├── deploy.py           # Production deployment script
│   ├── docker-compose.yml  # Multi-service deployment
│   ├── Dockerfile          # Container configuration
│   ├── nginx.conf          # Reverse proxy config
│   └── mongo-init.js       # Database initialization
├── frontend/               # React frontend (Production Ready)
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   │   ├── ui/        # shadcn/ui components
│   │   │   ├── AlertsPanel.tsx
│   │   │   ├── ThemeProvider.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── layouts/       # Layout components
│   │   │   ├── AuthLayout.tsx
│   │   │   └── DashboardLayout.tsx
│   │   ├── pages/         # Feature pages
│   │   │   ├── auth/      # Authentication pages
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── TrafficPage.tsx
│   │   │   ├── EnvironmentPage.tsx
│   │   │   ├── WastePage.tsx
│   │   │   ├── EnergyPage.tsx
│   │   │   ├── EmergencyPage.tsx
│   │   │   ├── AnalyticsPage.tsx
│   │   │   ├── AlertsPage.tsx
│   │   │   └── ProfilePage.tsx
│   │   ├── services/      # API & WebSocket services
│   │   │   ├── api.ts     # HTTP client & endpoints
│   │   │   └── websocket.ts
│   │   ├── store/         # Redux Toolkit store
│   │   │   ├── authSlice.ts
│   │   │   ├── dashboardSlice.ts
│   │   │   └── alertsSlice.ts
│   │   ├── hooks/         # Custom React hooks
│   │   │   ├── redux.ts
│   │   │   └── useWebSocket.ts
│   │   ├── lib/           # Utility functions
│   │   └── styles/        # Global styles
│   ├── Dockerfile         # Container configuration
│   ├── nginx.conf         # Production web server
│   ├── docker-compose.yml # Frontend deployment
│   ├── start.js           # Development startup script
│   └── package.json
├── deploy-full-stack.py    # Full-stack deployment script
├── docker-compose.yml      # Complete system deployment
├── SECURITY.md             # Security policy and guidelines
├── LICENSE                 # MIT License
└── README.md
```

## Modules

1. **Traffic Management**: Monitor traffic flow, optimize signal timing
2. **Environmental Monitoring**: Track air quality, noise levels
3. **Waste Management**: Optimize collection routes, monitor bin levels
4. **Energy Management**: Monitor grid usage, optimize distribution
5. **Emergency Response**: Coordinate emergency services, alert systems

## User Roles

- **Admin**: Full system access and configuration
- **Traffic Officer**: Traffic management and monitoring
- **Environment Officer**: Environmental data and alerts
- **Utility Officer**: Energy and waste management
- **Emergency Coordinator**: Emergency response coordination

## 🔒 Security

This project follows security best practices and includes:
- JWT authentication with role-based access control
- Input validation and sanitization
- Rate limiting and DDoS protection
- Secure password hashing with bcrypt
- HTTPS enforcement in production
- Docker security configurations

For security vulnerabilities, please see our [Security Policy](./SECURITY.md) and report issues to [contact@imraunak.dev](mailto:contact@imraunak.dev).

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   ```bash
   # Check if MongoDB is running
   sudo systemctl status mongod
   
   # Start MongoDB
   sudo systemctl start mongod
   ```

2. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   
   # Kill the process
   kill -9 <PID>
   ```

3. **Permission Denied**
   ```bash
   # Fix permissions
   chmod +x setup.py
   chmod +x start.py
   ```

4. **Frontend Build Issues**
   ```bash
   # Clear node modules and reinstall
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   
   # Clear Vite cache
   npm run dev -- --force
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

**Copyright (c) 2024 Pratham Upadhyay**

## 👨‍💻 Author

**Pratham Upadhyay**
- Email: [contact@imraunak.dev](mailto:contact@imraunak.dev)
- GitHub: [@raunak0400](https://github.com/raunak0400)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow the existing code style and conventions
- Add tests for new features
- Update documentation as needed
- Ensure security best practices are followed
- Run security scans before submitting PRs

## 📞 Support

For support and questions:
- **Email**: [contact@imraunak.dev](mailto:contact@imraunak.dev)
- **Issues**: Create an issue in the repository
- **Security**: See [SECURITY.md](./SECURITY.md) for security-related concerns

## 🙏 Acknowledgments

- Built with modern web technologies (React, Flask, MongoDB)
- UI components from [shadcn/ui](https://ui.shadcn.com/)
- Icons from [Lucide React](https://lucide.dev/)
- Charts powered by [Recharts](https://recharts.org/)
- Containerization with [Docker](https://www.docker.com/)

## 📊 Project Stats

- **Backend**: 9 API modules with 50+ endpoints
- **Frontend**: 9 feature pages with responsive design
- **Database**: MongoDB with optimized schemas
- **Security**: JWT auth with 5 role-based permissions
- **Real-time**: WebSocket integration for live updates
- **Deployment**: Full Docker containerization
- **Documentation**: Comprehensive guides and API docs

---

**Built with ❤️ by Raunak Kumar Jha for smart city management and urban optimization.**
