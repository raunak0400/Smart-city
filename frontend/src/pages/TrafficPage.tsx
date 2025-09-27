import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Car, 
  MapPin, 
  AlertTriangle, 
  Plus, 
  Filter,
  RefreshCw,
  Navigation,
  Clock,
  TrendingUp
} from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { trafficAPI } from '../services/api'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { formatDate } from '../lib/utils'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts'

const TrafficPage = () => {
  const [selectedTimeRange, setSelectedTimeRange] = useState('24h')
  const [showIncidentForm, setShowIncidentForm] = useState(false)
  const [incidentForm, setIncidentForm] = useState({
    type: '',
    location: '',
    severity: 'medium',
    description: ''
  })

  // Fetch traffic data
  const { data: trafficData, isLoading: trafficLoading, refetch: refetchTraffic } = useQuery({
    queryKey: ['traffic-data', selectedTimeRange],
    queryFn: () => trafficAPI.getTrafficData({ timeRange: selectedTimeRange }),
    refetchInterval: 30000,
  })

  const { data: incidents, isLoading: incidentsLoading, refetch: refetchIncidents } = useQuery({
    queryKey: ['traffic-incidents'],
    queryFn: () => trafficAPI.getIncidents({ status: 'active' }),
    refetchInterval: 15000,
  })

  // Mock data for charts
  const flowData = [
    { time: '00:00', northbound: 120, southbound: 95, eastbound: 80, westbound: 110 },
    { time: '06:00', northbound: 450, southbound: 380, eastbound: 320, westbound: 410 },
    { time: '12:00', northbound: 380, southbound: 420, eastbound: 290, westbound: 350 },
    { time: '18:00', northbound: 520, southbound: 480, eastbound: 410, westbound: 490 },
    { time: '23:59', northbound: 180, southbound: 160, eastbound: 140, westbound: 170 },
  ]

  const congestionData = [
    { intersection: 'Main & 1st', level: 85, avgDelay: 45 },
    { intersection: 'Oak & 2nd', level: 72, avgDelay: 32 },
    { intersection: 'Pine & 3rd', level: 68, avgDelay: 28 },
    { intersection: 'Elm & 4th', level: 91, avgDelay: 52 },
    { intersection: 'Cedar & 5th', level: 76, avgDelay: 38 },
  ]

  const handleIncidentSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await trafficAPI.reportIncident({
        ...incidentForm,
        reported_at: new Date().toISOString(),
        status: 'active'
      })
      setShowIncidentForm(false)
      setIncidentForm({ type: '', location: '', severity: 'medium', description: '' })
      refetchIncidents()
    } catch (error) {
      console.error('Failed to report incident:', error)
    }
  }

  const optimizeSignals = async () => {
    try {
      await trafficAPI.optimizeSignals({ intersections: 'all' })
      refetchTraffic()
    } catch (error) {
      console.error('Failed to optimize signals:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Traffic Management
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Real-time traffic monitoring and incident management
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => refetchTraffic()}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button onClick={() => setShowIncidentForm(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Report Incident
          </Button>
          <Button variant="secondary" onClick={optimizeSignals}>
            <Navigation className="h-4 w-4 mr-2" />
            Optimize Signals
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: 'Active Incidents', value: incidents?.length || 0, icon: AlertTriangle, color: 'text-red-600' },
          { title: 'Average Speed', value: '32 mph', icon: Car, color: 'text-blue-600' },
          { title: 'Traffic Volume', value: '2.4K/hr', icon: TrendingUp, color: 'text-green-600' },
          { title: 'Signal Efficiency', value: '87%', icon: Clock, color: 'text-purple-600' },
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
                  </div>
                  <stat.icon className={`h-8 w-8 ${stat.color}`} />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Traffic Flow Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center">
                <Car className="h-5 w-5 mr-2" />
                Traffic Flow by Direction
              </div>
              <select
                value={selectedTimeRange}
                onChange={(e) => setSelectedTimeRange(e.target.value)}
                className="text-sm border rounded px-2 py-1"
              >
                <option value="1h">Last Hour</option>
                <option value="24h">Last 24 Hours</option>
                <option value="7d">Last 7 Days</option>
              </select>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={flowData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="northbound" stroke="#3b82f6" strokeWidth={2} />
                <Line type="monotone" dataKey="southbound" stroke="#ef4444" strokeWidth={2} />
                <Line type="monotone" dataKey="eastbound" stroke="#10b981" strokeWidth={2} />
                <Line type="monotone" dataKey="westbound" stroke="#f59e0b" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Congestion Levels */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertTriangle className="h-5 w-5 mr-2" />
              Congestion Hotspots
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={congestionData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="intersection" angle={-45} textAnchor="end" height={80} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="level" fill="#ef4444" name="Congestion Level %" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Incidents and Map */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Incidents */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2" />
                Active Incidents
              </div>
              <span className="text-sm bg-red-100 text-red-800 px-2 py-1 rounded-full">
                {incidents?.length || 0}
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {incidentsLoading ? (
              <div className="flex justify-center py-8">
                <LoadingSpinner />
              </div>
            ) : (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {incidents?.map((incident: any) => (
                  <div key={incident.id} className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        {incident.type}
                      </h4>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        incident.severity === 'high' ? 'bg-red-100 text-red-800' :
                        incident.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {incident.severity}
                      </span>
                    </div>
                    <div className="flex items-center text-sm text-gray-600 dark:text-gray-400 mb-1">
                      <MapPin className="h-3 w-3 mr-1" />
                      {incident.location}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      {incident.description}
                    </p>
                    <div className="flex items-center text-xs text-gray-500 dark:text-gray-500">
                      <Clock className="h-3 w-3 mr-1" />
                      {formatDate(incident.reported_at)}
                    </div>
                  </div>
                )) || (
                  <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                    No active incidents
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Traffic Map Placeholder */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center">
              <MapPin className="h-5 w-5 mr-2" />
              Traffic Map
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-96 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
              <div className="text-center">
                <MapPin className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 dark:text-gray-400">
                  Interactive traffic map will be displayed here
                </p>
                <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
                  Showing real-time traffic flow, incidents, and signal status
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Incident Report Modal */}
      {showIncidentForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4"
          >
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Report Traffic Incident
            </h3>
            
            <form onSubmit={handleIncidentSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Incident Type
                </label>
                <select
                  value={incidentForm.type}
                  onChange={(e) => setIncidentForm({ ...incidentForm, type: e.target.value })}
                  className="w-full border rounded-md px-3 py-2"
                  required
                >
                  <option value="">Select type</option>
                  <option value="accident">Accident</option>
                  <option value="construction">Construction</option>
                  <option value="breakdown">Vehicle Breakdown</option>
                  <option value="weather">Weather Related</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Location
                </label>
                <Input
                  value={incidentForm.location}
                  onChange={(e) => setIncidentForm({ ...incidentForm, location: e.target.value })}
                  placeholder="e.g., Main St & 1st Ave"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Severity
                </label>
                <select
                  value={incidentForm.severity}
                  onChange={(e) => setIncidentForm({ ...incidentForm, severity: e.target.value })}
                  className="w-full border rounded-md px-3 py-2"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Description
                </label>
                <textarea
                  value={incidentForm.description}
                  onChange={(e) => setIncidentForm({ ...incidentForm, description: e.target.value })}
                  placeholder="Additional details about the incident"
                  rows={3}
                  className="w-full border rounded-md px-3 py-2"
                />
              </div>

              <div className="flex space-x-3 pt-4">
                <Button type="submit" className="flex-1">
                  Report Incident
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowIncidentForm(false)}
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

export default TrafficPage
