import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Zap, 
  Battery, 
  Sun, 
  Wind, 
  Droplets,
  TrendingUp,
  TrendingDown,
  RefreshCw,
  Settings,
  AlertTriangle,
  Activity
} from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { energyAPI } from '../services/api'
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

const EnergyPage = () => {
  const [selectedTimeRange, setSelectedTimeRange] = useState('24h')
  const [selectedGrid, setSelectedGrid] = useState('all')

  // Fetch energy data
  const { data: grids, isLoading: gridsLoading, refetch: refetchGrids } = useQuery({
    queryKey: ['energy-grids'],
    queryFn: () => energyAPI.getGrids(),
    refetchInterval: 60000, // Refetch every minute
  })

  const { data: consumption, isLoading: consumptionLoading } = useQuery({
    queryKey: ['energy-consumption', selectedTimeRange],
    queryFn: () => energyAPI.getConsumption({ timeRange: selectedTimeRange }),
    refetchInterval: 300000, // Refetch every 5 minutes
  })

  const { data: renewableData } = useQuery({
    queryKey: ['renewable-energy'],
    queryFn: () => energyAPI.getRenewableData(),
    refetchInterval: 300000,
  })

  // Mock data for charts
  const consumptionTrends = [
    { time: '00:00', residential: 850, commercial: 1200, industrial: 2100, total: 4150 },
    { time: '06:00', residential: 1200, commercial: 1800, industrial: 2800, total: 5800 },
    { time: '12:00', residential: 1100, commercial: 2200, industrial: 3200, total: 6500 },
    { time: '18:00', residential: 1800, commercial: 2500, industrial: 2900, total: 7200 },
    { time: '23:59', residential: 950, commercial: 1400, industrial: 2200, total: 4550 },
  ]

  const renewableGeneration = [
    { time: '00:00', solar: 0, wind: 450, hydro: 320, total: 770 },
    { time: '06:00', solar: 200, wind: 380, hydro: 320, total: 900 },
    { time: '12:00', solar: 850, wind: 420, hydro: 320, total: 1590 },
    { time: '18:00', solar: 320, wind: 480, hydro: 320, total: 1120 },
    { time: '23:59', solar: 0, wind: 520, hydro: 320, total: 840 },
  ]

  const energyMix = [
    { name: 'Solar', value: 28, color: '#fbbf24', capacity: '450 MW' },
    { name: 'Wind', value: 22, color: '#34d399', capacity: '380 MW' },
    { name: 'Hydro', value: 18, color: '#60a5fa', capacity: '320 MW' },
    { name: 'Natural Gas', value: 20, color: '#f87171', capacity: '420 MW' },
    { name: 'Nuclear', value: 12, color: '#a78bfa', capacity: '250 MW' },
  ]

  const gridStatus = [
    { id: 'GRID-001', name: 'North District', load: 85, capacity: 1200, status: 'normal', efficiency: 94 },
    { id: 'GRID-002', name: 'South District', load: 92, capacity: 1500, status: 'high', efficiency: 91 },
    { id: 'GRID-003', name: 'East District', load: 78, capacity: 1000, status: 'normal', efficiency: 96 },
    { id: 'GRID-004', name: 'West District', load: 88, capacity: 1300, status: 'normal', efficiency: 93 },
    { id: 'GRID-005', name: 'Industrial Zone', load: 95, capacity: 2000, status: 'critical', efficiency: 89 },
  ]

  const peakDemandForecast = [
    { hour: '00:00', predicted: 4200, actual: 4150 },
    { hour: '06:00', predicted: 5900, actual: 5800 },
    { hour: '12:00', predicted: 6400, actual: 6500 },
    { hour: '18:00', predicted: 7100, actual: 7200 },
    { hour: '23:59', predicted: 4600, actual: 4550 },
  ]

  const getLoadStatusColor = (load: number) => {
    if (load >= 95) return 'bg-red-500'
    if (load >= 85) return 'bg-yellow-500'
    return 'bg-green-500'
  }

  const getLoadStatusText = (load: number) => {
    if (load >= 95) return 'Critical'
    if (load >= 85) return 'High'
    return 'Normal'
  }

  const optimizeLoadBalancing = async () => {
    try {
      await energyAPI.optimizeLoadBalancing({ grids: 'all' })
      refetchGrids()
    } catch (error) {
      console.error('Failed to optimize load balancing:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Energy Management
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Grid monitoring, renewable energy tracking, and load optimization
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => refetchGrids()}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button variant="secondary" onClick={optimizeLoadBalancing}>
            <Settings className="h-4 w-4 mr-2" />
            Optimize Load
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

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
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
                    Total Consumption
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    6.2 MW
                  </p>
                  <div className="flex items-center mt-1">
                    <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                    <span className="text-xs text-green-600">+5% from yesterday</span>
                  </div>
                </div>
                <div className="p-3 rounded-full bg-blue-100">
                  <Zap className="h-6 w-6 text-blue-600" />
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
                    Renewable Share
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    68%
                  </p>
                  <div className="flex items-center mt-1">
                    <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                    <span className="text-xs text-green-600">+3% this month</span>
                  </div>
                </div>
                <div className="p-3 rounded-full bg-green-100">
                  <Sun className="h-6 w-6 text-green-600" />
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
                    Grid Efficiency
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    93%
                  </p>
                  <div className="flex items-center mt-1">
                    <TrendingDown className="h-3 w-3 text-red-500 mr-1" />
                    <span className="text-xs text-red-600">-1% from target</span>
                  </div>
                </div>
                <div className="p-3 rounded-full bg-purple-100">
                  <Activity className="h-6 w-6 text-purple-600" />
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
                    Peak Demand
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    7.2 MW
                  </p>
                  <div className="flex items-center mt-1">
                    <TrendingUp className="h-3 w-3 text-orange-500 mr-1" />
                    <span className="text-xs text-orange-600">At 6:00 PM</span>
                  </div>
                </div>
                <div className="p-3 rounded-full bg-orange-100">
                  <Battery className="h-6 w-6 text-orange-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Carbon Saved
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    2.4t
                  </p>
                  <div className="flex items-center mt-1">
                    <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
                    <span className="text-xs text-green-600">Today</span>
                  </div>
                </div>
                <div className="p-3 rounded-full bg-emerald-100">
                  <Wind className="h-6 w-6 text-emerald-600" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Energy Consumption Trends */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Zap className="h-5 w-5 mr-2" />
              Energy Consumption by Sector
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={consumptionTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area 
                  type="monotone" 
                  dataKey="residential" 
                  stackId="1" 
                  stroke="#3b82f6" 
                  fill="#3b82f6" 
                  fillOpacity={0.6}
                  name="Residential"
                />
                <Area 
                  type="monotone" 
                  dataKey="commercial" 
                  stackId="1" 
                  stroke="#10b981" 
                  fill="#10b981" 
                  fillOpacity={0.6}
                  name="Commercial"
                />
                <Area 
                  type="monotone" 
                  dataKey="industrial" 
                  stackId="1" 
                  stroke="#f59e0b" 
                  fill="#f59e0b" 
                  fillOpacity={0.6}
                  name="Industrial"
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Renewable Energy Generation */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Sun className="h-5 w-5 mr-2" />
              Renewable Energy Generation
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={renewableGeneration}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="solar" 
                  stroke="#fbbf24" 
                  strokeWidth={2}
                  name="Solar"
                />
                <Line 
                  type="monotone" 
                  dataKey="wind" 
                  stroke="#34d399" 
                  strokeWidth={2}
                  name="Wind"
                />
                <Line 
                  type="monotone" 
                  dataKey="hydro" 
                  stroke="#60a5fa" 
                  strokeWidth={2}
                  name="Hydro"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Energy Mix */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Battery className="h-5 w-5 mr-2" />
              Energy Mix
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={energyMix}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name} ${value}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {energyMix.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Grid Status */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Activity className="h-5 w-5 mr-2" />
              Grid Load Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {gridStatus.map((grid) => (
                <div key={grid.id} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className={`w-3 h-3 rounded-full ${getLoadStatusColor(grid.load)}`} />
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        {grid.name}
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {grid.id} • Capacity: {formatNumber(grid.capacity)} MW
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {grid.load}% Load
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {grid.efficiency}% Efficiency
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Demand Forecast and Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Peak Demand Forecast */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2" />
              Peak Demand Forecast vs Actual
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={peakDemandForecast}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="predicted" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  name="Predicted"
                />
                <Line 
                  type="monotone" 
                  dataKey="actual" 
                  stroke="#10b981" 
                  strokeWidth={2}
                  name="Actual"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Energy Alerts */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2" />
                Energy Alerts
              </div>
              <span className="text-sm bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                3 Active
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-medium text-red-800 dark:text-red-200">
                    Critical Load
                  </h4>
                  <span className="text-xs text-red-600 dark:text-red-400">
                    Now
                  </span>
                </div>
                <p className="text-sm text-red-700 dark:text-red-300 mb-2">
                  Industrial Zone grid at 95% capacity
                </p>
                <div className="flex items-center text-xs text-red-600 dark:text-red-400">
                  <Activity className="h-3 w-3 mr-1" />
                  GRID-005
                </div>
              </div>

              <div className="p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-medium text-yellow-800 dark:text-yellow-200">
                    High Demand
                  </h4>
                  <span className="text-xs text-yellow-600 dark:text-yellow-400">
                    15m ago
                  </span>
                </div>
                <p className="text-sm text-yellow-700 dark:text-yellow-300 mb-2">
                  South District approaching peak capacity
                </p>
                <div className="flex items-center text-xs text-yellow-600 dark:text-yellow-400">
                  <Activity className="h-3 w-3 mr-1" />
                  GRID-002
                </div>
              </div>

              <div className="p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-medium text-blue-800 dark:text-blue-200">
                    Maintenance Due
                  </h4>
                  <span className="text-xs text-blue-600 dark:text-blue-400">
                    Tomorrow
                  </span>
                </div>
                <p className="text-sm text-blue-700 dark:text-blue-300 mb-2">
                  Scheduled maintenance for Wind Farm B
                </p>
                <div className="flex items-center text-xs text-blue-600 dark:text-blue-400">
                  <Wind className="h-3 w-3 mr-1" />
                  Wind Farm B
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Renewable Energy Details */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Sun className="h-5 w-5 mr-2" />
            Renewable Energy Sources
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            {energyMix.map((source) => (
              <div key={source.name} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900 dark:text-white">
                    {source.name}
                  </h4>
                  <div 
                    className="w-4 h-4 rounded-full" 
                    style={{ backgroundColor: source.color }}
                  />
                </div>
                <div className="space-y-1">
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {source.value}%
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {source.capacity}
                  </p>
                  <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                    <div 
                      className="h-2 rounded-full" 
                      style={{ 
                        backgroundColor: source.color, 
                        width: `${source.value}%` 
                      }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default EnergyPage
