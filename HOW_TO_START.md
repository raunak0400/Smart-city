# 🚀 How to Start - Smart City Management Platform

This guide will help you run the Smart City Management Platform locally on your host machine for development.

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

1. **Python 3.11+**
   - Download from: https://www.python.org/downloads/
   - Verify: `python --version` or `python3 --version`

2. **Node.js 18+**
   - Download from: https://nodejs.org/
   - Verify: `node --version` and `npm --version`

3. **MongoDB Community Edition**
   - Download from: https://www.mongodb.com/try/download/community
   - Verify: `mongod --version`

4. **Git**
   - Download from: https://git-scm.com/downloads
   - Verify: `git --version`

### System Requirements

- **RAM**: At least 4GB available
- **Storage**: At least 2GB free space
- **Ports**: 3000, 5000, 27017 should be available

## 🛠️ Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd lode
```

### Step 2: Start MongoDB

**Windows:**
```cmd
# Start MongoDB service
net start MongoDB

# Or start manually
"C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe" --dbpath "C:\data\db"
```

**Linux/Mac:**
```bash
# Start MongoDB service
sudo systemctl start mongod

# Or start manually
mongod --dbpath /usr/local/var/mongodb
```

**Verify MongoDB is running:**
```bash
# Connect to MongoDB
mongosh
# You should see: "Current Mongosh Log ID: ..."
# Type 'exit' to quit
```

### Step 3: Setup Backend (Flask)

**Navigate to backend directory:**
```bash
cd backend
```

**Create Python virtual environment:**

*Windows:*
```cmd
python -m venv smart_city_env
smart_city_env\Scripts\activate
```

*Linux/Mac:*
```bash
python3 -m venv smart_city_env
source smart_city_env/bin/activate
```

**Install Python dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Setup environment variables:**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings (use any text editor)
notepad .env    # Windows
nano .env       # Linux/Mac
```

**Key environment variables to configure:**
```env
# Database Configuration
MONGO_URI=mongodb://localhost:27017/smart_city_db
MONGO_DB_NAME=smart_city_db

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=3600

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-flask-secret-key-change-in-production
```

**Initialize the database:**
```bash
python setup.py
```

**Start the backend server:**
```bash
# Option 1: Using the start script (recommended)
python start.py

# Option 2: Using Flask directly
flask run --host=0.0.0.0 --port=5000

# Option 3: Using the app directly
python app.py
```

**Verify backend is running:**
- Open browser: http://localhost:5000/api/health
- You should see: `{"status": "healthy", "timestamp": "..."}`

### Step 4: Setup Frontend (React)

**Open a new terminal/command prompt and navigate to frontend:**
```bash
cd frontend
```

**Install Node.js dependencies:**
```bash
npm install
```

**Setup environment variables:**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file
notepad .env    # Windows
nano .env       # Linux/Mac
```

**Key environment variables to configure:**
```env
# API Configuration
VITE_API_BASE_URL=http://localhost:5000/api
VITE_WS_URL=http://localhost:5000

# Application Configuration
VITE_APP_NAME=Smart City Management Platform
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_NOTIFICATIONS=true
VITE_ENABLE_DARK_MODE=true
```

**Start the frontend development server:**
```bash
# Option 1: Using the start script (recommended)
node start.js

# Option 2: Using npm directly
npm run dev

# Option 3: Using Vite directly
npx vite
```

**Verify frontend is running:**
- Open browser: http://localhost:3000
- You should see the Smart City Management Platform login page

## 🎯 Quick Start Commands

### Windows Quick Start

**Terminal 1 (Backend):**
```cmd
cd backend
smart_city_env\Scripts\activate
python start.py
```

**Terminal 2 (Frontend):**
```cmd
cd frontend
node start.js
```

### Linux/Mac Quick Start

**Terminal 1 (Backend):**
```bash
cd backend
source smart_city_env/bin/activate
python start.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
node start.js
```

## 🌐 Access Your Application

Once both services are running:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **API Documentation**: http://localhost:5000/api/docs (if available)
- **MongoDB**: localhost:27017

### Default Login Credentials

```
Email: admin@smartcity.com
Password: admin123
```

## 🔧 Development Workflow

### Making Changes

**Backend Changes:**
1. Edit Python files in `/backend/src/`
2. The server will auto-reload (if using `python start.py`)
3. Check logs in terminal for any errors

**Frontend Changes:**
1. Edit React files in `/frontend/src/`
2. Vite will auto-reload the browser
3. Check browser console for any errors

### Database Management

**View MongoDB data:**
```bash
mongosh
use smart_city_db
show collections
db.users.find()
```

**Reset database:**
```bash
cd backend
python setup.py --reset
```

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**

*Error: "Port 3000/5000 is already in use"*

**Solution:**
```bash
# Windows - Find and kill process
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F

# Linux/Mac - Find and kill process
lsof -i :3000
kill -9 <PID_NUMBER>
```

**2. MongoDB Connection Failed**

*Error: "MongoServerError: Authentication failed"*

**Solution:**
```bash
# Check if MongoDB is running
mongosh

# If authentication issues, update .env:
MONGO_URI=mongodb://localhost:27017/smart_city_db
```

**3. Python Module Not Found**

*Error: "ModuleNotFoundError: No module named 'flask'"*

**Solution:**
```bash
# Ensure virtual environment is activated
cd backend
# Windows
smart_city_env\Scripts\activate
# Linux/Mac
source smart_city_env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**4. Node Modules Issues**

*Error: "Cannot resolve dependency" or "Module not found"*

**Solution:**
```bash
cd frontend
# Clear cache and reinstall
rm -rf node_modules package-lock.json  # Linux/Mac
rmdir /s node_modules & del package-lock.json  # Windows

npm install
```

**5. Environment Variables Not Loading**

*Error: API calls failing or configuration issues*

**Solution:**
```bash
# Check .env files exist
ls backend/.env frontend/.env  # Linux/Mac
dir backend\.env frontend\.env  # Windows

# Ensure no extra spaces in .env files
# Restart both servers after .env changes
```

### Debug Mode

**Enable detailed logging:**

*Backend:*
```bash
export FLASK_DEBUG=True  # Linux/Mac
set FLASK_DEBUG=True     # Windows
python app.py
```

*Frontend:*
```bash
export VITE_DEBUG=true   # Linux/Mac
set VITE_DEBUG=true      # Windows
npm run dev
```

### Performance Issues

**Slow startup:**
- Ensure you have enough RAM (4GB+)
- Close unnecessary applications
- Use SSD storage if possible

**API calls timing out:**
- Check backend logs for errors
- Verify MongoDB is running
- Check network connectivity

## 📁 Project Structure

```
lode/
├── backend/                 # Flask backend
│   ├── src/                # Source code
│   ├── .env               # Environment variables
│   ├── requirements.txt   # Python dependencies
│   ├── start.py          # Development server
│   └── app.py            # Main application
├── frontend/               # React frontend
│   ├── src/               # Source code
│   ├── .env              # Environment variables
│   ├── package.json      # Node dependencies
│   └── start.js          # Development server
└── README.md             # This file
```

## 🔄 Stopping the Application

**To stop the servers:**
1. Press `Ctrl+C` in each terminal window
2. Deactivate Python virtual environment: `deactivate`
3. Stop MongoDB service if needed:
   - Windows: `net stop MongoDB`
   - Linux/Mac: `sudo systemctl stop mongod`

## 🚀 Next Steps

Once you have the application running:

1. **Explore the Features:**
   - Traffic Management
   - Environmental Monitoring
   - Waste Management
   - Energy Management
   - Emergency Response

2. **Development:**
   - Check `/backend/src/` for API endpoints
   - Check `/frontend/src/` for React components
   - Review the database schema in MongoDB

3. **Testing:**
   - Create test users and data
   - Test different user roles
   - Verify real-time features work

## 📞 Need Help?

If you encounter issues:

1. **Check the logs** in both terminal windows
2. **Verify all prerequisites** are installed correctly
3. **Ensure all ports** (3000, 5000, 27017) are available
4. **Check environment variables** in both `.env` files
5. **Restart services** in the correct order: MongoDB → Backend → Frontend

---

**Happy Development! 🎉**

Your Smart City Management Platform should now be running locally and ready for development!
