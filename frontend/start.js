#!/usr/bin/env node

const { execSync, spawn } = require('child_process')
const fs = require('fs')
const path = require('path')

console.log('🚀 Smart City Frontend Startup Script')
console.log('=' .repeat(50))

// Check if Node.js version is compatible
const nodeVersion = process.version
const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0])

if (majorVersion < 16) {
  console.error('❌ Node.js version 16 or higher is required')
  console.error(`Current version: ${nodeVersion}`)
  process.exit(1)
}

console.log(`✅ Node.js version: ${nodeVersion}`)

// Check if package.json exists
if (!fs.existsSync('package.json')) {
  console.error('❌ package.json not found. Please run this script from the frontend directory.')
  process.exit(1)
}

// Check if .env file exists, create from .env.example if not
if (!fs.existsSync('.env')) {
  if (fs.existsSync('.env.example')) {
    fs.copyFileSync('.env.example', '.env')
    console.log('✅ Created .env file from .env.example')
    console.log('⚠️  Please review and update the .env file with your configuration')
  } else {
    console.log('⚠️  No .env file found. Using default environment variables.')
  }
}

// Check if node_modules exists
if (!fs.existsSync('node_modules')) {
  console.log('📦 Installing dependencies...')
  try {
    execSync('npm install', { stdio: 'inherit' })
    console.log('✅ Dependencies installed successfully')
  } catch (error) {
    console.error('❌ Failed to install dependencies')
    console.error(error.message)
    process.exit(1)
  }
} else {
  console.log('✅ Dependencies already installed')
}

// Check if backend is running
console.log('🔍 Checking backend connectivity...')
const backendUrl = process.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

try {
  const { execSync } = require('child_process')
  execSync(`curl -f ${backendUrl.replace('/api', '')}/api/health`, { 
    stdio: 'pipe',
    timeout: 5000 
  })
  console.log('✅ Backend is running and accessible')
} catch (error) {
  console.log('⚠️  Backend is not accessible. Make sure to start the backend first:')
  console.log('   cd ../backend')
  console.log('   python start.py')
  console.log('')
  console.log('Continuing with frontend startup...')
}

// Start the development server
console.log('')
console.log('🎯 Starting React development server...')
console.log('Frontend will be available at: http://localhost:3000')
console.log('Press Ctrl+C to stop the server')
console.log('')

try {
  const devServer = spawn('npm', ['run', 'dev'], {
    stdio: 'inherit',
    shell: true
  })

  // Handle process termination
  process.on('SIGINT', () => {
    console.log('\n👋 Shutting down frontend server...')
    devServer.kill('SIGINT')
    process.exit(0)
  })

  process.on('SIGTERM', () => {
    devServer.kill('SIGTERM')
    process.exit(0)
  })

  devServer.on('close', (code) => {
    if (code !== 0) {
      console.error(`❌ Development server exited with code ${code}`)
      process.exit(code)
    }
  })

} catch (error) {
  console.error('❌ Failed to start development server')
  console.error(error.message)
  process.exit(1)
}
