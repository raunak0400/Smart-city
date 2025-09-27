import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Leaf, 
  Wind, 
  Thermometer, 
  Droplets, 
  AlertTriangle,
  TrendingUp,
  TrendingDown,
  RefreshCw,
  MapPin,
  Calendar
} from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { environmentAPI } from '../services/api'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { formatDate } from '../lib/utils'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'

const EnvironmentPage = () => {
  const [selectedTimeRange, setSelectedTimeRange] = useState('24h')
  const [selectedMetric, setSelectedMetric] = useState('aqi')

  // Fetch environment data
  const { data: environmentData, isLoading, refetch } = useQuery({
    queryKey: ['environment-data', selectedTimeRange],
    queryFn: () => environmentAPI.getEnvironmentData({ timeRange: selectedTimeRange }),
    refetchInterval: 60000, // Refetch every minute
  })

  const { data: airQualitySummary } = useQuery({
    queryKey: ['air-quality-summary'],
    queryFn: environmentAPI.getAirQualitySummary,
    refetchInterval: 300000, // Refetch every 5 minutes
  })

  const { data: pollutionTrends } = useQuery({
    queryKey: ['pollution-trends', selectedTimeRange],
    queryFn: () => environmentAPI.getPollutionTrends({ timeRange: selectedTimeRange }),
    refetchInterval: 300000,
  })

  // Mock data for charts
  const aqiData = [
    { time: '00:00', aqi: 45, pm25: 12, pm10: 18, no2: 25, o3: 35 },
    { time: '04:00', aqi: 52, pm25: 15, pm10: 22, no2: 28, o3: 38 },
    { time: '08:00', aqi: 68, pm25: 22, pm10: 35, no2: 45, o3: 42 },
    { time: '12:00', aqi: 58, pm25: 18, pm10: 28, no2: 38, o3: 48 },
    { time: '16:00', aqi: 72, pm25: 25, pm10: 38, no2: 52, o3: 45 },
    { time: '20:00', aqi: 48, pm25: 14, pm10: 22, no2: 32, o3: 38 },
  ]

  const sensorData = [
    { location: 'Downtown', aqi: 68, pm25: 22, temperature: 24, humidity: 65, status: 'moderate' },
    { location: 'Industrial Zone', aqi: 85, pm25: 35, temperature: 26, humidity: 58, status: 'unhealthy' },
    { location: 'Residential Area', aqi: 42, pm25: 12, temperature: 23, humidity: 72, status: 'good' },
    { location: 'Park District', aqi: 35, pm25: 8, temperature: 22, humidity: 78, status: 'good' },
    { location: 'Highway Corridor', aqi: 78, pm25: 28, temperature: 25, humidity: 62, status: 'moderate' },
  ]

  const weeklyTrends = [
    { day: 'Mon', aqi: 45, pm25: 12, no2: 25, temperature: 22 },
    { day: 'Tue', aqi: 52, pm25: 15, no2: 28, temperature: 24 },
    { day: 'Wed', aqi: 38, pm25: 10, no2: 22, temperature: 21 },
    { day: 'Thu', aqi: 41, pm25: 11, no2: 24, temperature: 23 },
    { day: 'Fri', aqi: 48, pm25: 13, no2: 26, temperature: 25 },
    { day: 'Sat', aqi: 35, pm25: 9, no2: 20, temperature: 20 },
    { day: 'Sun', aqi: 42, pm25: 12, no2: 23, temperature: 22 },
  ]

  const getAQIStatus = (aqi: number) => {
    if (aqi <= 50) return { status: 'Good', color: 'text-green-600', bgColor: 'bg-green-100' }
    if (aqi <= 100) return { status: 'Moderate', color: 'text-yellow-600', bgColor: 'bg-yellow-100' }
    if (aqi <= 150) return { status: 'Unhealthy for Sensitive', color: 'text-orange-600', bgColor: 'bg-orange-100' }
    if (aqi <= 200) return { status: 'Unhealthy', color: 'text-red-600', bgColor: 'bg-red-100' }
    return { status: 'Very Unhealthy', color: 'text-purple-600', bgColor: 'bg-purple-100' }
  }

  const currentAQI = 58
  const aqiStatus = getAQIStatus(currentAQI)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Environmental Monitoring
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Real-time air quality and environmental data monitoring
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => refetch()}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh Data
          </Button>
          <select
            value={selectedTimeRange}
            onChange={(e) => setSelectedTimeRange(e.target.value)}
            className="border rounded-md px-3 py-2 text-sm"
          >
            <option value="1h">Last Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>
        </div>
      </div>

      {/* Current Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Air Quality Index
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {currentAQI}
                  </p>
                  <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${aqiStatus.bgColor} ${aqiStatus.color}`}>
                    {aqiStatus.status}
                  </div>
                </div>
                <div className="p-3 rounded-full bg-green-100">
                  <Leaf className="h-6 w-6 text-green-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    PM2.5 Level
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    18 μg/m³
                  </p>
                  <div className="flex items-center mt-1">
                    <TrendingDown className="h-3 w-3 text-green-500 mr-1" />
                    <span className="text-xs text-green-600">-12% from yesterday</span>
                  </div>
                </div>
                <div className="p-3 rounded-full bg-blue-100">
                  <Wind className="h-6 w-6 text-blue-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Temperature
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    24°C
                  </p>
                  <div className="flex items-center mt-1">
                    <TrendingUp className="h-3 w-3 text-orange-500 mr-1" />
                    <span className="text-xs text-orange-600">+2°C from morning</span>
                  </div>
                </div>
                <div className="p-3 rounded-full bg-orange-100">
                  <Thermometer className="h-6 w-6 text-orange-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Humidity
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    68%
                  </p>
                  <div className="flex items-center mt-1">
                    <TrendingDown className="h-3 w-3 text-blue-500 mr-1" />
                    <span className="text-xs text-blue-600">-5% from yesterday</span>
                  </div>
                </div>
                <div className="p-3 rounded-full bg-cyan-100">
                  <Droplets className="h-6 w-6 text-cyan-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Real-time AQI Trends */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center">
                <Leaf className="h-5 w-5 mr-2" />
                Air Quality Trends
              </div>
              <select
                value={selectedMetric}
                onChange={(e) => setSelectedMetric(e.target.value)}
                className="text-sm border rounded px-2 py-1"
              >
                <option value="aqi">AQI</option>
                <option value="pm25">PM2.5</option>
                <option value="pm10">PM10</option>
                <option value="no2">NO2</option>
                <option value="o3">O3</option>
              </select>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={aqiData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Area 
                  type="monotone" 
                  dataKey={selectedMetric} 
                  stroke="#10b981" 
                  fill="#10b981" 
                  fillOpacity={0.6}
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Weekly Comparison */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              Weekly Environmental Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={weeklyTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="aqi" stroke="#10b981" strokeWidth={2} name="AQI" />
                <Line type="monotone" dataKey="pm25" stroke="#f59e0b" strokeWidth={2} name="PM2.5" />
                <Line type="monotone" dataKey="temperature" stroke="#ef4444" strokeWidth={2} name="Temperature" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Sensor Locations and Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sensor Locations */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center">
              <MapPin className="h-5 w-5 mr-2" />
              Monitoring Stations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {sensorData.map((sensor, index) => (
                <div key={sensor.location} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className={`w-3 h-3 rounded-full ${
                      sensor.status === 'good' ? 'bg-green-500' :
                      sensor.status === 'moderate' ? 'bg-yellow-500' : 'bg-red-500'
                    }`} />
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        {sensor.location}
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        AQI: {sensor.aqi} • PM2.5: {sensor.pm25} μg/m³
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {sensor.temperature}°C
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {sensor.humidity}% humidity
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Environmental Alerts */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2" />
                Environmental Alerts
              </div>
              <span className="text-sm bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                2 Active
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-medium text-yellow-800 dark:text-yellow-200">
                    High PM2.5 Levels
                  </h4>
                  <span className="text-xs text-yellow-600 dark:text-yellow-400">
                    2h ago
                  </span>
                </div>
                <p className="text-sm text-yellow-700 dark:text-yellow-300 mb-2">
                  PM2.5 levels exceeded 35 μg/m³ in Industrial Zone
                </p>
                <div className="flex items-center text-xs text-yellow-600 dark:text-yellow-400">
                  <MapPin className="h-3 w-3 mr-1" />
                  Industrial Zone Station
                </div>
              </div>

              <div className="p-3 bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-medium text-orange-800 dark:text-orange-200">
                    Air Quality Moderate
                  </h4>
                  <span className="text-xs text-orange-600 dark:text-orange-400">
                    4h ago
                  </span>
                </div>
                <p className="text-sm text-orange-700 dark:text-orange-300 mb-2">
                  AQI reached 78 in Highway Corridor area
                </p>
                <div className="flex items-center text-xs text-orange-600 dark:text-orange-400">
                  <MapPin className="h-3 w-3 mr-1" />
                  Highway Corridor Station
                </div>
              </div>

              <div className="text-center py-4">
                <Button variant="outline" size="sm">
                  View All Alerts
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Pollutant Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Wind className="h-5 w-5 mr-2" />
            Pollutant Breakdown
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={aqiData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="pm25" fill="#f59e0b" name="PM2.5" />
              <Bar dataKey="pm10" fill="#ef4444" name="PM10" />
              <Bar dataKey="no2" fill="#8b5cf6" name="NO2" />
              <Bar dataKey="o3" fill="#06b6d4" name="O3" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}

export default EnvironmentPage
