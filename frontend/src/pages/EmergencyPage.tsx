import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  AlertTriangle, 
  Siren, 
  MapPin, 
  Clock, 
  Phone,
  Truck,
  Users,
  Radio,
  Plus,
  RefreshCw,
  Send
} from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { emergencyAPI } from '../services/api'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { formatDate } from '../lib/utils'

const EmergencyPage = () => {
  const [showIncidentForm, setShowIncidentForm] = useState(false)
  const [showBroadcastForm, setShowBroadcastForm] = useState(false)
  const [incidentForm, setIncidentForm] = useState({
    type: '',
    severity: 'medium',
    location: '',
    description: '',
    requiredUnits: []
  })
  const [broadcastForm, setBroadcastForm] = useState({
    type: 'warning',
    message: '',
    areas: [],
    channels: ['sms', 'app']
  })

  // Fetch emergency data
  const { data: incidents, isLoading: incidentsLoading, refetch: refetchIncidents } = useQuery({
    queryKey: ['emergency-incidents'],
    queryFn: () => emergencyAPI.getIncidents({ status: 'active' }),
    refetchInterval: 30000, // Refetch every 30 seconds
  })

  const { data: units, isLoading: unitsLoading, refetch: refetchUnits } = useQuery({
    queryKey: ['emergency-units'],
    queryFn: () => emergencyAPI.getUnits(),
    refetchInterval: 60000, // Refetch every minute
  })

  // Mock data
  const responseTimeStats = [
    { type: 'Fire', avgTime: '4.2 min', target: '5 min', status: 'good' },
    { type: 'Medical', avgTime: '3.8 min', target: '4 min', status: 'good' },
    { type: 'Police', avgTime: '6.1 min', target: '6 min', status: 'warning' },
    { type: 'Rescue', avgTime: '8.5 min', target: '8 min', status: 'warning' },
  ]

  const emergencyUnits = [
    { id: 'FIRE-001', type: 'Fire Truck', status: 'available', location: 'Station 1', crew: 4 },
    { id: 'FIRE-002', type: 'Fire Truck', status: 'dispatched', location: 'En Route', crew: 4 },
    { id: 'AMB-001', type: 'Ambulance', status: 'available', location: 'Hospital', crew: 2 },
    { id: 'AMB-002', type: 'Ambulance', status: 'busy', location: 'Emergency Call', crew: 2 },
    { id: 'POL-001', type: 'Police Unit', status: 'available', location: 'Patrol Area A', crew: 2 },
    { id: 'POL-002', type: 'Police Unit', status: 'dispatched', location: 'Downtown', crew: 2 },
    { id: 'RES-001', type: 'Rescue Team', status: 'available', location: 'Base', crew: 6 },
  ]

  const activeIncidents = [
    {
      id: 'INC-001',
      type: 'Building Fire',
      severity: 'high',
      location: 'Main St & 5th Ave',
      reportedAt: '2024-01-15T14:30:00Z',
      status: 'active',
      unitsDispatched: ['FIRE-002', 'AMB-002'],
      description: 'Structure fire in commercial building'
    },
    {
      id: 'INC-002',
      type: 'Traffic Accident',
      severity: 'medium',
      location: 'Highway 101 Mile 15',
      reportedAt: '2024-01-15T14:45:00Z',
      status: 'active',
      unitsDispatched: ['POL-002'],
      description: 'Multi-vehicle collision, injuries reported'
    },
    {
      id: 'INC-003',
      type: 'Medical Emergency',
      severity: 'high',
      location: 'City Park',
      reportedAt: '2024-01-15T15:00:00Z',
      status: 'responding',
      unitsDispatched: ['AMB-001'],
      description: 'Cardiac arrest, CPR in progress'
    }
  ]

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'text-red-600 bg-red-100'
      case 'high': return 'text-orange-600 bg-orange-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getUnitStatusColor = (status: string) => {
    switch (status) {
      case 'available': return 'text-green-600 bg-green-100'
      case 'dispatched': return 'text-blue-600 bg-blue-100'
      case 'busy': return 'text-yellow-600 bg-yellow-100'
      case 'maintenance': return 'text-gray-600 bg-gray-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const handleIncidentSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await emergencyAPI.createIncident({
        ...incidentForm,
        reported_at: new Date().toISOString(),
        status: 'active'
      })
      setShowIncidentForm(false)
      setIncidentForm({ type: '', severity: 'medium', location: '', description: '', requiredUnits: [] })
      refetchIncidents()
    } catch (error) {
      console.error('Failed to create incident:', error)
    }
  }

  const handleBroadcastSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await emergencyAPI.broadcastAlert({
        ...broadcastForm,
        timestamp: new Date().toISOString()
      })
      setShowBroadcastForm(false)
      setBroadcastForm({ type: 'warning', message: '', areas: [], channels: ['sms', 'app'] })
    } catch (error) {
      console.error('Failed to broadcast alert:', error)
    }
  }

  const dispatchUnit = async (unitId: string, incidentId: string) => {
    try {
      await emergencyAPI.dispatchUnit(unitId, incidentId)
      refetchUnits()
      refetchIncidents()
    } catch (error) {
      console.error('Failed to dispatch unit:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Emergency Response
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Incident management, unit dispatch, and emergency coordination
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => refetchIncidents()}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button onClick={() => setShowIncidentForm(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Report Incident
          </Button>
          <Button variant="secondary" onClick={() => setShowBroadcastForm(true)}>
            <Radio className="h-4 w-4 mr-2" />
            Broadcast Alert
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: 'Active Incidents', value: activeIncidents.length, icon: AlertTriangle, color: 'text-red-600' },
          { title: 'Available Units', value: emergencyUnits.filter(u => u.status === 'available').length, icon: Truck, color: 'text-green-600' },
          { title: 'Dispatched Units', value: emergencyUnits.filter(u => u.status === 'dispatched').length, icon: Siren, color: 'text-blue-600' },
          { title: 'Avg Response Time', value: '4.8 min', icon: Clock, color: 'text-purple-600' },
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

      {/* Active Incidents and Units */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Active Incidents */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <div className="flex items-center">
                <AlertTriangle className="h-5 w-5 mr-2" />
                Active Incidents
              </div>
              <span className="text-sm bg-red-100 text-red-800 px-2 py-1 rounded-full">
                {activeIncidents.length} Active
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {activeIncidents.map((incident) => (
                <div key={incident.id} className="p-4 border rounded-lg bg-white dark:bg-gray-700">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        {incident.type}
                      </h4>
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(incident.severity)}`}>
                        {incident.severity.toUpperCase()}
                      </span>
                    </div>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {incident.id}
                    </span>
                  </div>
                  
                  <div className="space-y-2 mb-3">
                    <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                      <MapPin className="h-3 w-3 mr-1" />
                      {incident.location}
                    </div>
                    <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                      <Clock className="h-3 w-3 mr-1" />
                      {formatDate(incident.reportedAt)}
                    </div>
                    <p className="text-sm text-gray-700 dark:text-gray-300">
                      {incident.description}
                    </p>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        Units: {incident.unitsDispatched.join(', ')}
                      </span>
                    </div>
                    <Button size="sm" variant="outline">
                      View Details
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Emergency Units */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Truck className="h-5 w-5 mr-2" />
              Emergency Units
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {emergencyUnits.map((unit) => (
                <div key={unit.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full ${
                      unit.status === 'available' ? 'bg-green-500' :
                      unit.status === 'dispatched' ? 'bg-blue-500' :
                      unit.status === 'busy' ? 'bg-yellow-500' : 'bg-gray-500'
                    }`} />
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        {unit.id}
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {unit.type} • {unit.crew} crew
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getUnitStatusColor(unit.status)}`}>
                      {unit.status}
                    </span>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {unit.location}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Response Time Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Clock className="h-5 w-5 mr-2" />
            Response Time Analysis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {responseTimeStats.map((stat) => (
              <div key={stat.type} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900 dark:text-white">
                    {stat.type}
                  </h4>
                  <div className={`w-3 h-3 rounded-full ${
                    stat.status === 'good' ? 'bg-green-500' : 'bg-yellow-500'
                  }`} />
                </div>
                <div className="space-y-1">
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {stat.avgTime}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Target: {stat.target}
                  </p>
                  <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                    <div className={`h-2 rounded-full ${
                      stat.status === 'good' ? 'bg-green-500' : 'bg-yellow-500'
                    }`} style={{ width: '85%' }} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Emergency Map Placeholder */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <MapPin className="h-5 w-5 mr-2" />
            Emergency Response Map
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-96 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center">
            <div className="text-center">
              <MapPin className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500 dark:text-gray-400">
                Interactive map showing incidents, units, and response routes
              </p>
              <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
                Real-time tracking of emergency vehicles and incident locations
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Report Incident Modal */}
      {showIncidentForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4"
          >
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Report Emergency Incident
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
                  <option value="fire">Fire</option>
                  <option value="medical">Medical Emergency</option>
                  <option value="accident">Traffic Accident</option>
                  <option value="crime">Crime in Progress</option>
                  <option value="natural_disaster">Natural Disaster</option>
                  <option value="hazmat">Hazardous Materials</option>
                  <option value="other">Other</option>
                </select>
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
                  <option value="critical">Critical</option>
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
                  Description
                </label>
                <textarea
                  value={incidentForm.description}
                  onChange={(e) => setIncidentForm({ ...incidentForm, description: e.target.value })}
                  placeholder="Detailed description of the incident"
                  rows={3}
                  className="w-full border rounded-md px-3 py-2"
                  required
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

      {/* Broadcast Alert Modal */}
      {showBroadcastForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4"
          >
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Broadcast Emergency Alert
            </h3>
            
            <form onSubmit={handleBroadcastSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Alert Type
                </label>
                <select
                  value={broadcastForm.type}
                  onChange={(e) => setBroadcastForm({ ...broadcastForm, type: e.target.value })}
                  className="w-full border rounded-md px-3 py-2"
                >
                  <option value="warning">Warning</option>
                  <option value="evacuation">Evacuation</option>
                  <option value="shelter">Shelter in Place</option>
                  <option value="all_clear">All Clear</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Message
                </label>
                <textarea
                  value={broadcastForm.message}
                  onChange={(e) => setBroadcastForm({ ...broadcastForm, message: e.target.value })}
                  placeholder="Emergency alert message to broadcast"
                  rows={4}
                  className="w-full border rounded-md px-3 py-2"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Broadcast Channels
                </label>
                <div className="space-y-2">
                  {['SMS', 'Mobile App', 'Email', 'Radio', 'TV'].map((channel) => (
                    <label key={channel} className="flex items-center">
                      <input
                        type="checkbox"
                        checked={broadcastForm.channels.includes(channel.toLowerCase())}
                        onChange={(e) => {
                          const channelId = channel.toLowerCase()
                          if (e.target.checked) {
                            setBroadcastForm({
                              ...broadcastForm,
                              channels: [...broadcastForm.channels, channelId]
                            })
                          } else {
                            setBroadcastForm({
                              ...broadcastForm,
                              channels: broadcastForm.channels.filter(c => c !== channelId)
                            })
                          }
                        }}
                        className="mr-2"
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300">
                        {channel}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="flex space-x-3 pt-4">
                <Button type="submit" className="flex-1">
                  <Send className="h-4 w-4 mr-2" />
                  Broadcast Alert
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowBroadcastForm(false)}
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

export default EmergencyPage
