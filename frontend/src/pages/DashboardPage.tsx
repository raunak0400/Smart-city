import { useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Activity, 
  AlertTriangle, 
  Car, 
  Leaf, 
  Trash2, 
  Zap,
  TrendingUp,
  TrendingDown,
  Users,
  MapPin
} from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { useAppDispatch, useAppSelector } from '../hooks/redux'
import { fetchDashboardOverview, fetchRealTimeData } from '../store/dashboardSlice'
import { fetchAlerts } from '../store/alertsSlice'
import { dashboardAPI } from '../services/api'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { formatNumber } from '../lib/utils'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'

const DashboardPage = () => {
  const dispatch = useAppDispatch()
  const { stats, realTimeData, isLoading, lastUpdated } = useAppSelector((state) => state.dashboard)
  const { activeAlerts } = useAppSelector((state) => state.alerts)

  // Fetch dashboard data
  const { data: overviewData } = useQuery({
    queryKey: ['dashboard-overview'],
    queryFn: dashboardAPI.getOverview,
    refetchInterval: 30000, // Refetch every 30 seconds
  })

  const { data: weeklyStats } = useQuery({
    queryKey: ['weekly-statistics'],
    queryFn: dashboardAPI.getWeeklyStatistics,
    refetchInterval: 60000, // Refetch every minute
  })

  useEffect(() => {
    dispatch(fetchDashboardOverview())
    dispatch(fetchRealTimeData())
    dispatch(fetchAlerts({ status: 'active', limit: 10 }))
  }, [dispatch])

  // Mock data for charts
  const trafficData = [
    { time: '00:00', flow: 120, congestion: 15 },
    { time: '06:00', flow: 450, congestion: 35 },
    { time: '12:00', flow: 380, congestion: 25 },
    { time: '18:00', flow: 520, congestion: 45 },
    { time: '23:59', flow: 180, congestion: 20 },
  ]

  const energyData = [
    { name: 'Solar', value: 35, color: '#fbbf24' },
    { name: 'Wind', value: 25, color: '#34d399' },
    { name: 'Hydro', value: 20, color: '#60a5fa' },
    { name: 'Grid', value: 20, color: '#f87171' },
  ]

  const airQualityData = [
    { day: 'Mon', aqi: 45, pm25: 12, pm10: 18 },
    { day: 'Tue', aqi: 52, pm25: 15, pm10: 22 },
    { day: 'Wed', aqi: 38, pm25: 10, pm10: 16 },
    { day: 'Thu', aqi: 41, pm25: 11, pm10: 19 },
    { day: 'Fri', aqi: 48, pm25: 13, pm10: 21 },
    { day: 'Sat', aqi: 35, pm25: 9, pm10: 15 },
    { day: 'Sun', aqi: 42, pm25: 12, pm10: 18 },
  ]

  const kpiCards = [
    {
      title: 'Active Alerts',
      value: activeAlerts.length,
      change: '+12%',
      trend: 'up',
      icon: AlertTriangle,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
    },
    {
      title: 'Traffic Flow',
      value: '2.4K',
      change: '+8%',
      trend: 'up',
      icon: Car,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
    },
    {
      title: 'Air Quality Index',
      value: '42',
      change: '-5%',
      trend: 'down',
      icon: Leaf,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
    },
    {
      title: 'Waste Collection',
      value: '89%',
      change: '+3%',
      trend: 'up',
      icon: Trash2,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100',
    },
    {
      title: 'Energy Usage',
      value: '1.2MW',
      change: '-2%',
      trend: 'down',
      icon: Zap,
      color: 'text-yellow-600',
      bgColor: 'bg-yellow-100',
    },
    {
      title: 'System Health',
      value: '98.5%',
      change: '+0.2%',
      trend: 'up',
      icon: Activity,
      color: 'text-emerald-600',
      bgColor: 'bg-emerald-100',
    },
  ]

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Dashboard Overview
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Real-time city infrastructure monitoring and management
          </p>
        </div>
        <div className="text-sm text-gray-500 dark:text-gray-400">
          Last updated: {lastUpdated ? new Date(lastUpdated).toLocaleTimeString() : 'Never'}
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {kpiCards.map((kpi, index) => (
          <motion.div
            key={kpi.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      {kpi.title}
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      {kpi.value}
                    </p>
                    <div className="flex items-center mt-1">
                      {kpi.trend === 'up' ? (
                        <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                      ) : (
                        <TrendingDown className="h-3 w-3 text-red-500 mr-1" />
                      )}
                      <span className={`text-xs ${kpi.trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                        {kpi.change}
                      </span>
                    </div>
                  </div>
                  <div className={`p-3 rounded-full ${kpi.bgColor}`}>
                    <kpi.icon className={`h-6 w-6 ${kpi.color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Traffic Flow Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Car className="h-5 w-5 mr-2" />
              Traffic Flow & Congestion
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trafficData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="flow" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  name="Traffic Flow"
                />
                <Line 
                  type="monotone" 
                  dataKey="congestion" 
                  stroke="#ef4444" 
                  strokeWidth={2}
                  name="Congestion %"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Energy Distribution */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Zap className="h-5 w-5 mr-2" />
              Energy Sources Distribution
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={energyData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {energyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Air Quality Trends */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Leaf className="h-5 w-5 mr-2" />
              Air Quality Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={airQualityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="aqi" 
                  stackId="1" 
                  stroke="#10b981" 
                  fill="#10b981" 
                  fillOpacity={0.6}
                  name="AQI"
                />
                <Area 
                  type="monotone" 
                  dataKey="pm25" 
                  stackId="2" 
                  stroke="#f59e0b" 
                  fill="#f59e0b" 
                  fillOpacity={0.6}
                  name="PM2.5"
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Recent Alerts */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2" />
                Recent Alerts
              </div>
              <Button variant="outline" size="sm">
                View All
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {activeAlerts.slice(0, 5).map((alert) => (
                <div key={alert.id} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className={`w-2 h-2 rounded-full mt-2 ${
                    alert.severity === 'critical' ? 'bg-red-500' :
                    alert.severity === 'high' ? 'bg-orange-500' :
                    alert.severity === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
                  }`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                      {alert.alert_type}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                      {alert.message}
                    </p>
                    <p className="text-xs text-gray-400 dark:text-gray-500">
                      {new Date(alert.created_at).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
              
              {activeAlerts.length === 0 && (
                <div className="text-center py-4 text-gray-500 dark:text-gray-400">
                  No active alerts
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* System Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Activity className="h-5 w-5 mr-2" />
            System Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { name: 'Traffic Sensors', status: 'online', count: 245 },
              { name: 'Air Quality Monitors', status: 'online', count: 89 },
              { name: 'Waste Bins', status: 'online', count: 1240 },
              { name: 'Energy Meters', status: 'online', count: 156 },
            ].map((system) => (
              <div key={system.name} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div>
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {system.name}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {system.count} devices
                  </p>
                </div>
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-green-500 rounded-full mr-2" />
                  <span className="text-xs text-green-600 dark:text-green-400 font-medium">
                    {system.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default DashboardPage
