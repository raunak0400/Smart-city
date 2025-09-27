# Smart City Management Platform - Frontend

A modern, responsive React frontend for the Smart City Management Platform with real-time monitoring capabilities and role-based access control.

## 🚀 Features

### 🎨 Modern UI/UX
- **React 18** with TypeScript for type safety
- **Tailwind CSS** for utility-first styling
- **shadcn/ui** components for consistent design
- **Framer Motion** for smooth animations
- **Dark/Light theme** support
- **Fully responsive** design (mobile, tablet, desktop)

### 🔐 Authentication & Security
- **JWT-based authentication** with refresh tokens
- **Role-based access control** (Admin, Traffic Officer, Environment Officer, etc.)
- **Protected routes** with permission checks
- **Secure token storage** and automatic refresh

### 📊 Real-time Dashboard
- **Live KPI monitoring** with auto-refresh
- **Interactive charts** using Recharts
- **WebSocket integration** for real-time updates
- **Alert notifications** with severity-based styling
- **Performance metrics** and trend analysis

### 🏗️ Feature Modules
- **Traffic Management** - Flow monitoring, incident reporting, signal optimization
- **Environmental Monitoring** - Air quality tracking, pollution trends, sensor data
- **Waste Management** - Smart bin monitoring, collection optimization, route planning
- **Energy Management** - Grid monitoring, renewable energy tracking, load balancing
- **Emergency Response** - Incident management, unit dispatch, alert broadcasting
- **Analytics & Reports** - Predictive analytics, KPI dashboards, comprehensive reporting

### 🔔 Notifications & Alerts
- **Real-time alert panel** with WebSocket updates
- **Toast notifications** for critical events
- **Alert management** with acknowledge/resolve actions
- **Notification preferences** per user

## 🛠️ Tech Stack

- **Frontend Framework**: React 18 + Vite + TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **State Management**: Redux Toolkit + React Query
- **Routing**: React Router v6
- **HTTP Client**: Axios with interceptors
- **Real-time**: Socket.IO client
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Forms**: React Hook Form + Zod validation
- **Build Tool**: Vite
- **Linting**: ESLint + Prettier
- **Deployment**: Docker + Nginx

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── ui/           # shadcn/ui components
│   │   ├── AlertsPanel.tsx
│   │   ├── ThemeProvider.tsx
│   │   └── ProtectedRoute.tsx
│   ├── layouts/          # Layout components
│   │   ├── AuthLayout.tsx
│   │   └── DashboardLayout.tsx
│   ├── pages/            # Page components
│   │   ├── auth/         # Authentication pages
│   │   ├── DashboardPage.tsx
│   │   ├── TrafficPage.tsx
│   │   ├── EnvironmentPage.tsx
│   │   ├── WastePage.tsx
│   │   ├── EnergyPage.tsx
│   │   ├── EmergencyPage.tsx
│   │   ├── AnalyticsPage.tsx
│   │   ├── AlertsPage.tsx
│   │   └── ProfilePage.tsx
│   ├── services/         # API services
│   │   ├── api.ts        # HTTP client & API calls
│   │   └── websocket.ts  # WebSocket service
│   ├── store/            # Redux store
│   │   ├── index.ts
│   │   ├── authSlice.ts
│   │   ├── dashboardSlice.ts
│   │   └── alertsSlice.ts
│   ├── hooks/            # Custom hooks
│   │   ├── redux.ts
│   │   └── useWebSocket.ts
│   ├── lib/              # Utility functions
│   │   └── utils.ts
│   ├── styles/           # Global styles
│   │   └── globals.css
│   ├── App.tsx           # Main app component
│   └── main.tsx          # App entry point
├── Dockerfile            # Container configuration
├── nginx.conf            # Nginx configuration
├── docker-compose.yml    # Multi-service deployment
├── package.json          # Dependencies & scripts
├── tailwind.config.js    # Tailwind configuration
├── vite.config.ts        # Vite configuration
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- Backend API running on http://localhost:5000

### Installation

1. **Clone and install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Open in browser:**
   ```
   http://localhost:3000
   ```

### Default Login Credentials
- **Admin**: admin@smartcity.com / admin123
- **Traffic Officer**: traffic@smartcity.com / traffic123
- **Environment Officer**: env@smartcity.com / env123

## 🐳 Docker Deployment

### Development
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t smart-city-frontend .
docker run -p 3000:80 smart-city-frontend
```

### Production
```bash
# Build production image
docker build -t smart-city-frontend:prod .

# Run with environment variables
docker run -d \
  -p 80:80 \
  -e VITE_API_BASE_URL=https://api.smartcity.com/api \
  -e VITE_WS_URL=https://api.smartcity.com \
  smart-city-frontend:prod
```

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:5000/api
VITE_WS_URL=http://localhost:5000

# Application Settings
VITE_APP_NAME=Smart City Management Platform
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_NOTIFICATIONS=true

# External Services (Optional)
VITE_GOOGLE_MAPS_API_KEY=your-api-key
VITE_SENTRY_DSN=your-sentry-dsn
```

### API Integration
The frontend connects to the Flask backend via:
- **REST API**: HTTP requests for CRUD operations
- **WebSocket**: Real-time updates for alerts and live data
- **Authentication**: JWT tokens with automatic refresh

## 📱 Features by Role

### 👑 Administrator
- Full access to all modules and analytics
- User management and system configuration
- Comprehensive reporting and KPI monitoring
- System health and performance metrics

### 🚦 Traffic Officer
- Traffic flow monitoring and incident management
- Signal optimization and route planning
- Traffic pattern analysis and reporting
- Real-time congestion alerts

### 🌱 Environment Officer
- Air quality monitoring and pollution tracking
- Environmental sensor management
- Pollution trend analysis and forecasting
- Environmental alert management

### 🗑️ Utility Officer
- Waste bin monitoring and collection scheduling
- Route optimization and efficiency tracking
- Energy grid monitoring and load balancing
- Utility performance analytics

### 🚨 Emergency Coordinator
- Emergency incident management and response
- Unit dispatch and coordination
- Public alert broadcasting
- Response time analysis and optimization

## 🎨 UI Components

### Core Components
- **Dashboard Cards**: KPI metrics with trend indicators
- **Interactive Charts**: Line, bar, pie, and radar charts
- **Data Tables**: Sortable, filterable tables with pagination
- **Alert Panels**: Real-time alert management interface
- **Forms**: Validated forms with error handling
- **Modals**: Overlay dialogs for detailed views

### Design System
- **Colors**: Consistent color palette with semantic meanings
- **Typography**: Clear hierarchy with readable fonts
- **Spacing**: Consistent spacing scale using Tailwind
- **Icons**: Lucide React icons for consistency
- **Animations**: Smooth transitions with Framer Motion

## 🔄 Real-time Features

### WebSocket Events
```javascript
// Connection events
socket.on('connect', () => console.log('Connected'))
socket.on('disconnect', () => console.log('Disconnected'))

// Alert events
socket.on('new_alert', (alert) => updateAlerts(alert))
socket.on('alert_acknowledged', (data) => updateAlertStatus(data))
socket.on('alert_resolved', (data) => updateAlertStatus(data))

// Data updates
socket.on('traffic_update', (data) => updateTrafficData(data))
socket.on('environment_update', (data) => updateEnvironmentData(data))
socket.on('emergency_alert', (incident) => showEmergencyAlert(incident))
```

### Auto-refresh Intervals
- **Dashboard KPIs**: Every 30 seconds
- **Charts & Graphs**: Every 1-5 minutes
- **Alert Status**: Real-time via WebSocket
- **System Health**: Every 2 minutes

## 📊 Performance

### Optimization Features
- **Code splitting** with React.lazy()
- **Image optimization** with proper formats
- **Bundle analysis** with Vite bundle analyzer
- **Caching strategies** for API responses
- **Lazy loading** for charts and heavy components

### Lighthouse Scores (Target)
- **Performance**: ≥ 90
- **Accessibility**: ≥ 95
- **Best Practices**: ≥ 90
- **SEO**: ≥ 85

## 🧪 Testing

### Running Tests
```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Coverage report
npm run test:coverage
```

### Testing Strategy
- **Unit tests** for utility functions and hooks
- **Component tests** for UI components
- **Integration tests** for API interactions
- **E2E tests** for critical user flows

## 🚀 Deployment

### Build for Production
```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

### Deployment Options
1. **Docker Container** (Recommended)
2. **Static hosting** (Netlify, Vercel)
3. **CDN deployment** (AWS CloudFront)
4. **Traditional web server** (Apache, Nginx)

### CI/CD Pipeline
```yaml
# Example GitHub Actions workflow
name: Deploy Frontend
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - run: docker build -t frontend .
      - run: docker push registry/frontend
```

## 🔍 Monitoring & Analytics

### Error Tracking
- **Sentry integration** for error monitoring
- **Console logging** with different levels
- **Performance monitoring** with Web Vitals
- **User analytics** with privacy compliance

### Health Checks
- **API connectivity** monitoring
- **WebSocket connection** status
- **Performance metrics** tracking
- **User session** monitoring

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### Code Standards
- **TypeScript** for type safety
- **ESLint + Prettier** for code formatting
- **Conventional commits** for commit messages
- **Component documentation** with JSDoc

## 📚 API Documentation

### Authentication Endpoints
```typescript
// Login
POST /api/auth/login
Body: { email: string, password: string }
Response: { access_token: string, user: User }

// Get Profile
GET /api/auth/profile
Headers: { Authorization: "Bearer <token>" }
Response: { user: User }
```

### Real-time Events
```typescript
// Subscribe to alerts
socket.emit('subscribe_alerts', {
  severity_levels: ['high', 'critical'],
  modules: ['traffic', 'emergency']
})

// Join dashboard room
socket.emit('join_room', { room: 'dashboard' })
```

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**
   ```bash
   # Check if backend is running
   curl http://localhost:5000/api/health
   
   # Verify environment variables
   echo $VITE_API_BASE_URL
   ```

2. **WebSocket Connection Issues**
   ```bash
   # Check WebSocket URL
   echo $VITE_WS_URL
   
   # Verify backend WebSocket support
   curl -H "Upgrade: websocket" http://localhost:5000/socket.io/
   ```

3. **Build Errors**
   ```bash
   # Clear node modules and reinstall
   rm -rf node_modules package-lock.json
   npm install
   
   # Clear Vite cache
   npm run dev -- --force
   ```

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Create GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: support@smartcity.com

---

Built with ❤️ for smart city management and monitoring.
