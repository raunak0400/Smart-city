import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Bell, 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  Filter,
  Search,
  RefreshCw,
  Settings,
  Download,
  Eye,
  X
} from 'lucide-react'
import { useAppDispatch, useAppSelector } from '../hooks/redux'
import { fetchAlerts, acknowledgeAlert, resolveAlert, bulkAcknowledge, setFilters } from '../store/alertsSlice'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { formatDate, getSeverityColor, getStatusColor } from '../lib/utils'

const AlertsPage = () => {
  const dispatch = useAppDispatch()
  const { alerts, isLoading, filters } = useAppSelector((state) => state.alerts)
  const [selectedAlerts, setSelectedAlerts] = useState<string[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [showFilters, setShowFilters] = useState(false)
  const [selectedAlert, setSelectedAlert] = useState<any>(null)

  useEffect(() => {
    dispatch(fetchAlerts(filters))
  }, [dispatch, filters])

  // Filter alerts based on search term
  const filteredAlerts = alerts.filter(alert =>
    alert.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
    alert.alert_type.toLowerCase().includes(searchTerm.toLowerCase()) ||
    alert.module.toLowerCase().includes(searchTerm.toLowerCase())
  )

  // Group alerts by status
  const alertsByStatus = {
    active: filteredAlerts.filter(alert => alert.status === 'active'),
    acknowledged: filteredAlerts.filter(alert => alert.status === 'acknowledged'),
    resolved: filteredAlerts.filter(alert => alert.status === 'resolved')
  }

  const handleFilterChange = (key: string, value: string) => {
    dispatch(setFilters({ [key]: value }))
  }

  const handleSelectAlert = (alertId: string) => {
    setSelectedAlerts(prev => 
      prev.includes(alertId) 
        ? prev.filter(id => id !== alertId)
        : [...prev, alertId]
    )
  }

  const handleSelectAll = () => {
    if (selectedAlerts.length === filteredAlerts.length) {
      setSelectedAlerts([])
    } else {
      setSelectedAlerts(filteredAlerts.map(alert => alert.id))
    }
  }

  const handleBulkAcknowledge = async () => {
    if (selectedAlerts.length > 0) {
      await dispatch(bulkAcknowledge(selectedAlerts))
      setSelectedAlerts([])
    }
  }

  const handleAcknowledge = async (alertId: string) => {
    await dispatch(acknowledgeAlert(alertId))
  }

  const handleResolve = async (alertId: string) => {
    await dispatch(resolveAlert({ alertId }))
  }

  const exportAlerts = () => {
    // Implementation for exporting alerts
    console.log('Exporting alerts...')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Alerts Management
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Monitor, acknowledge, and resolve system alerts
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => dispatch(fetchAlerts(filters))}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button variant="outline" onClick={exportAlerts}>
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button variant="outline" onClick={() => setShowFilters(!showFilters)}>
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { 
            title: 'Active Alerts', 
            value: alertsByStatus.active.length, 
            icon: AlertTriangle, 
            color: 'text-red-600',
            bgColor: 'bg-red-100'
          },
          { 
            title: 'Acknowledged', 
            value: alertsByStatus.acknowledged.length, 
            icon: Clock, 
            color: 'text-yellow-600',
            bgColor: 'bg-yellow-100'
          },
          { 
            title: 'Resolved', 
            value: alertsByStatus.resolved.length, 
            icon: CheckCircle, 
            color: 'text-green-600',
            bgColor: 'bg-green-100'
          },
          { 
            title: 'Total Alerts', 
            value: filteredAlerts.length, 
            icon: Bell, 
            color: 'text-blue-600',
            bgColor: 'bg-blue-100'
          },
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
                  <div className={`p-3 rounded-full ${stat.bgColor}`}>
                    <stat.icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Search and Filters */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col space-y-4">
            {/* Search Bar */}
            <div className="flex items-center space-x-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search alerts by message, type, or module..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              {selectedAlerts.length > 0 && (
                <Button onClick={handleBulkAcknowledge}>
                  Acknowledge Selected ({selectedAlerts.length})
                </Button>
              )}
            </div>

            {/* Filters */}
            {showFilters && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="grid grid-cols-1 md:grid-cols-4 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700"
              >
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Status
                  </label>
                  <select
                    value={filters.status}
                    onChange={(e) => handleFilterChange('status', e.target.value)}
                    className="w-full border rounded-md px-3 py-2 text-sm"
                  >
                    <option value="">All Status</option>
                    <option value="active">Active</option>
                    <option value="acknowledged">Acknowledged</option>
                    <option value="resolved">Resolved</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Severity
                  </label>
                  <select
                    value={filters.severity}
                    onChange={(e) => handleFilterChange('severity', e.target.value)}
                    className="w-full border rounded-md px-3 py-2 text-sm"
                  >
                    <option value="">All Severities</option>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="critical">Critical</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Module
                  </label>
                  <select
                    value={filters.module}
                    onChange={(e) => handleFilterChange('module', e.target.value)}
                    className="w-full border rounded-md px-3 py-2 text-sm"
                  >
                    <option value="">All Modules</option>
                    <option value="traffic">Traffic</option>
                    <option value="environment">Environment</option>
                    <option value="waste">Waste</option>
                    <option value="energy">Energy</option>
                    <option value="emergency">Emergency</option>
                  </select>
                </div>

                <div className="flex items-end">
                  <Button
                    variant="outline"
                    onClick={() => {
                      dispatch(setFilters({ status: '', severity: '', module: '' }))
                      setSearchTerm('')
                    }}
                    className="w-full"
                  >
                    Clear Filters
                  </Button>
                </div>
              </motion.div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Alerts Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center">
              <Bell className="h-5 w-5 mr-2" />
              Alerts ({filteredAlerts.length})
            </div>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={selectedAlerts.length === filteredAlerts.length && filteredAlerts.length > 0}
                onChange={handleSelectAll}
                className="rounded"
              />
              <span className="text-sm text-gray-600 dark:text-gray-400">
                Select All
              </span>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex justify-center py-8">
              <LoadingSpinner size="lg" />
            </div>
          ) : filteredAlerts.length === 0 ? (
            <div className="text-center py-8">
              <Bell className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500 dark:text-gray-400">
                No alerts found matching your criteria
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-200 dark:border-gray-700">
                    <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">
                      <input
                        type="checkbox"
                        checked={selectedAlerts.length === filteredAlerts.length}
                        onChange={handleSelectAll}
                        className="rounded"
                      />
                    </th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Alert</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Severity</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Module</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Status</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Created</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredAlerts.map((alert) => (
                    <tr key={alert.id} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="py-3 px-4">
                        <input
                          type="checkbox"
                          checked={selectedAlerts.includes(alert.id)}
                          onChange={() => handleSelectAlert(alert.id)}
                          className="rounded"
                        />
                      </td>
                      <td className="py-3 px-4">
                        <div>
                          <p className="font-medium text-gray-900 dark:text-white">
                            {alert.alert_type}
                          </p>
                          <p className="text-gray-600 dark:text-gray-400 text-xs">
                            {alert.message}
                          </p>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)}`}>
                          {alert.severity.toUpperCase()}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-gray-900 dark:text-white capitalize">
                          {alert.module}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(alert.status)}`}>
                          {alert.status}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-gray-600 dark:text-gray-400">
                        {formatDate(alert.created_at)}
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex space-x-2">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => setSelectedAlert(alert)}
                          >
                            <Eye className="h-3 w-3" />
                          </Button>
                          {alert.status === 'active' && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleAcknowledge(alert.id)}
                            >
                              Acknowledge
                            </Button>
                          )}
                          <Button
                            size="sm"
                            onClick={() => handleResolve(alert.id)}
                          >
                            Resolve
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Alert Detail Modal */}
      {selectedAlert && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Alert Details
              </h3>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setSelectedAlert(null)}
              >
                <X className="h-5 w-5" />
              </Button>
            </div>

            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Alert ID
                  </label>
                  <p className="text-sm text-gray-900 dark:text-white">{selectedAlert.id}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Type
                  </label>
                  <p className="text-sm text-gray-900 dark:text-white">{selectedAlert.alert_type}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Severity
                  </label>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(selectedAlert.severity)}`}>
                    {selectedAlert.severity.toUpperCase()}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Status
                  </label>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedAlert.status)}`}>
                    {selectedAlert.status}
                  </span>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Message
                </label>
                <p className="text-sm text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700 p-3 rounded">
                  {selectedAlert.message}
                </p>
              </div>

              {selectedAlert.location && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Location
                  </label>
                  <p className="text-sm text-gray-900 dark:text-white">{selectedAlert.location}</p>
                </div>
              )}

              {selectedAlert.affected_systems && selectedAlert.affected_systems.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Affected Systems
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {selectedAlert.affected_systems.map((system: string, index: number) => (
                      <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                        {system}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {selectedAlert.recommended_actions && selectedAlert.recommended_actions.length > 0 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Recommended Actions
                  </label>
                  <ul className="text-sm text-gray-900 dark:text-white space-y-1">
                    {selectedAlert.recommended_actions.map((action: string, index: number) => (
                      <li key={index} className="flex items-start">
                        <span className="mr-2">•</span>
                        <span>{action}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Created At
                  </label>
                  <p className="text-gray-900 dark:text-white">{formatDate(selectedAlert.created_at)}</p>
                </div>
                {selectedAlert.acknowledged_at && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Acknowledged At
                    </label>
                    <p className="text-gray-900 dark:text-white">{formatDate(selectedAlert.acknowledged_at)}</p>
                  </div>
                )}
              </div>

              <div className="flex space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
                {selectedAlert.status === 'active' && (
                  <Button
                    onClick={() => {
                      handleAcknowledge(selectedAlert.id)
                      setSelectedAlert(null)
                    }}
                    className="flex-1"
                  >
                    Acknowledge
                  </Button>
                )}
                <Button
                  onClick={() => {
                    handleResolve(selectedAlert.id)
                    setSelectedAlert(null)
                  }}
                  variant={selectedAlert.status === 'active' ? 'outline' : 'default'}
                  className="flex-1"
                >
                  Resolve
                </Button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  )
}

export default AlertsPage
