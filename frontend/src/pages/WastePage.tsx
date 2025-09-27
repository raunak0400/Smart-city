import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Trash2, 
  MapPin, 
  Truck, 
  Calendar, 
  TrendingUp,
  AlertTriangle,
  RefreshCw,
  Plus,
  Route,
  Clock
} from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { wasteAPI } from '../services/api'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { formatDate } from '../lib/utils'
import {
  BarChart,
  Bar,
  LineChart,
  Line,
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

const WastePage = () => {
  const [selectedTimeRange, setSelectedTimeRange] = useState('24h')
  const [showScheduleForm, setShowScheduleForm] = useState(false)

  // Fetch waste data
  const { data: bins, isLoading: binsLoading, refetch: refetchBins } = useQuery({
    queryKey: ['waste-bins'],
    queryFn: () => wasteAPI.getBins(),
    refetchInterval: 300000, // Refetch every 5 minutes
  })

  const { data: collections, isLoading: collectionsLoading } = useQuery({
    queryKey: ['waste-collections', selectedTimeRange],
    queryFn: () => wasteAPI.getCollections({ timeRange: selectedTimeRange }),
    refetchInterval: 600000, // Refetch every 10 minutes
  })

  // Mock data for charts
  const binLevelData = [
    { area: 'Downtown', empty: 12, half: 18, full: 8, overflowing: 2 },
    { area: 'Residential', empty: 25, half: 32, full: 15, overflowing: 3 },
    { area: 'Industrial', empty: 8, half: 12, full: 6, overflowing: 1 },
    { area: 'Commercial', empty: 15, half: 22, full: 12, overflowing: 4 },
    { area: 'Parks', empty: 18, half: 14, full: 5, overflowing: 1 },
  ]

  const collectionTrends = [
    { day: 'Mon', collected: 45, scheduled: 50, efficiency: 90 },
    { day: 'Tue', collected: 52, scheduled: 55, efficiency: 95 },
    { day: 'Wed', collected: 48, scheduled: 52, efficiency: 92 },
    { day: 'Thu', collected: 58, scheduled: 60, efficiency: 97 },
    { day: 'Fri', collected: 62, scheduled: 65, efficiency: 95 },
    { day: 'Sat', collected: 38, scheduled: 40, efficiency: 95 },
    { day: 'Sun', collected: 28, scheduled: 30, efficiency: 93 },
  ]

  const wasteTypeData = [
    { name: 'General Waste', value: 45, color: '#6b7280' },
    { name: 'Recyclables', value: 30, color: '#10b981' },
    { name: 'Organic', value: 20, color: '#f59e0b' },
    { name: 'Hazardous', value: 5, color: '#ef4444' },
  ]

  const routeOptimization = [
    { route: 'Route A', bins: 25, distance: '12.5 km', time: '2.5h', efficiency: 92 },
    { route: 'Route B', bins: 32, distance: '18.2 km', time: '3.2h', efficiency: 88 },
    { route: 'Route C', bins: 28, distance: '15.8 km', time: '2.8h', efficiency: 95 },
    { route: 'Route D', bins: 22, distance: '10.3 km', time: '2.1h', efficiency: 98 },
  ]

  const getBinStatusColor = (level: number) => {
    if (level >= 90) return 'bg-red-500'
    if (level >= 70) return 'bg-yellow-500'
    if (level >= 40) return 'bg-blue-500'
    return 'bg-green-500'
  }

  const getBinStatusText = (level: number) => {
    if (level >= 90) return 'Critical'
    if (level >= 70) return 'High'
    if (level >= 40) return 'Medium'
    return 'Low'
  }

  const optimizeRoutes = async () => {
    try {
      await wasteAPI.optimizeRoutes({ area: 'all' })
      // Refresh data after optimization
      refetchBins()
    } catch (error) {
      console.error('Failed to optimize routes:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Waste Management
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Smart bin monitoring and collection optimization
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => refetchBins()}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button onClick={() => setShowScheduleForm(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Schedule Collection
          </Button>
          <Button variant="secondary" onClick={optimizeRoutes}>
            <Route className="h-4 w-4 mr-2" />
            Optimize Routes
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: 'Total Bins', value: '1,247', icon: Trash2, color: 'text-blue-600', change: '+12' },
          { title: 'Full Bins', value: '89', icon: AlertTriangle, color: 'text-red-600', change: '-5' },
          { title: 'Collections Today', value: '156', icon: Truck, color: 'text-green-600', change: '+8' },
          { title: 'Route Efficiency', value: '94%', icon: Route, color: 'text-purple-600', change: '+2%' },
        ].map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                      {stat.title}
                    </p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      {stat.value}
                    </p>
                    <p className="text-xs text-green-600">
                      {stat.change} from yesterday
                    </p>
                  </div>
                  <stat.icon className={`h-8 w-8 ${stat.color}`} />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bin Status by Area */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Trash2 className="h-5 w-5 mr-2" />
              Bin Status by Area
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={binLevelData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="area" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="empty" stackId="a" fill="#10b981" name="Empty" />
                <Bar dataKey="half" stackId="a" fill="#3b82f6" name="Half Full" />
                <Bar dataKey="full" stackId="a" fill="#f59e0b" name="Full" />
                <Bar dataKey="overflowing" stackId="a" fill="#ef4444" name="Overflowing" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Collection Efficiency */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Truck className="h-5 w-5 mr-2" />
              Collection Efficiency
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={collectionTrends}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="collected" 
                  stroke="#10b981" 
                  strokeWidth={2}
                  name="Collected"
                />
                <Line 
                  type="monotone" 
                  dataKey="scheduled" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  name="Scheduled"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Waste Type Distribution */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2" />
              Waste Type Distribution
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={wasteTypeData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {wasteTypeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Route Optimization */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Route className="h-5 w-5 mr-2" />
              Route Optimization Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {routeOptimization.map((route) => (
                <div key={route.route} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className={`w-3 h-3 rounded-full ${
                      route.efficiency >= 95 ? 'bg-green-500' :
                      route.efficiency >= 90 ? 'bg-yellow-500' : 'bg-red-500'
                    }`} />
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        {route.route}
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {route.bins} bins • {route.distance} • {route.time}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {route.efficiency}%
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Efficiency
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Bin Status Map and Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Bin Status Map Placeholder */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center">
              <MapPin className="h-5 w-5 mr-2" />
              Smart Bin Locations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-96 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <MapPin className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 dark:text-gray-400">
                  Interactive map showing bin locations and status
                </p>
                <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
                  Color-coded by fill level and collection priority
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Critical Bins */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2" />
                Critical Bins
              </div>
              <span className="text-sm bg-red-100 text-red-800 px-2 py-1 rounded-full">
                12 Critical
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {[
                { id: 'BIN-001', location: 'Main St & 1st Ave', level: 95, type: 'General' },
                { id: 'BIN-045', location: 'Park Plaza', level: 92, type: 'Recyclable' },
                { id: 'BIN-078', location: 'Shopping Center', level: 98, type: 'General' },
                { id: 'BIN-123', location: 'City Hall', level: 88, type: 'Organic' },
                { id: 'BIN-156', location: 'Bus Terminal', level: 94, type: 'General' },
              ].map((bin) => (
                <div key={bin.id} className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-medium text-red-800 dark:text-red-200">
                      {bin.id}
                    </h4>
                    <span className={`w-3 h-3 rounded-full ${getBinStatusColor(bin.level)}`} />
                  </div>
                  <div className="flex items-center text-sm text-red-700 dark:text-red-300 mb-1">
                    <MapPin className="h-3 w-3 mr-1" />
                    {bin.location}
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-red-600 dark:text-red-400">
                      {bin.type} Waste
                    </span>
                    <span className="font-medium text-red-800 dark:text-red-200">
                      {bin.level}% Full
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Collection Schedule */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              Today's Collection Schedule
            </div>
            <Button variant="outline" size="sm">
              View Full Schedule
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { time: '06:00', route: 'Route A', status: 'completed', bins: 25, driver: 'John D.' },
              { time: '08:30', route: 'Route B', status: 'in-progress', bins: 32, driver: 'Sarah M.' },
              { time: '11:00', route: 'Route C', status: 'scheduled', bins: 28, driver: 'Mike R.' },
              { time: '14:00', route: 'Route D', status: 'scheduled', bins: 22, driver: 'Lisa K.' },
            ].map((schedule) => (
              <div key={schedule.route} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900 dark:text-white">
                    {schedule.route}
                  </h4>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    schedule.status === 'completed' ? 'bg-green-100 text-green-800' :
                    schedule.status === 'in-progress' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {schedule.status}
                  </span>
                </div>
                <div className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                  <div className="flex items-center">
                    <Clock className="h-3 w-3 mr-1" />
                    {schedule.time}
                  </div>
                  <div className="flex items-center">
                    <Trash2 className="h-3 w-3 mr-1" />
                    {schedule.bins} bins
                  </div>
                  <div className="flex items-center">
                    <Truck className="h-3 w-3 mr-1" />
                    {schedule.driver}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Schedule Collection Modal */}
      {showScheduleForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4"
          >
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Schedule Collection
            </h3>
            
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Route
                </label>
                <select className="w-full border rounded-md px-3 py-2">
                  <option value="">Select route</option>
                  <option value="route-a">Route A</option>
                  <option value="route-b">Route B</option>
                  <option value="route-c">Route C</option>
                  <option value="route-d">Route D</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Date & Time
                </label>
                <input
                  type="datetime-local"
                  className="w-full border rounded-md px-3 py-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Driver
                </label>
                <select className="w-full border rounded-md px-3 py-2">
                  <option value="">Select driver</option>
                  <option value="john">John D.</option>
                  <option value="sarah">Sarah M.</option>
                  <option value="mike">Mike R.</option>
                  <option value="lisa">Lisa K.</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Priority
                </label>
                <select className="w-full border rounded-md px-3 py-2">
                  <option value="normal">Normal</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>

              <div className="flex space-x-3 pt-4">
                <Button type="submit" className="flex-1">
                  Schedule Collection
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowScheduleForm(false)}
                  className="flex-1"
                >
                  Cancel
                </Button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </div>
  )
}

export default WastePage
