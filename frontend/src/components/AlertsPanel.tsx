import { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, AlertTriangle, CheckCircle, Clock } from 'lucide-react'
import { useAppDispatch, useAppSelector } from '../hooks/redux'
import { fetchAlerts, acknowledgeAlert, resolveAlert } from '../store/alertsSlice'
import { Button } from './ui/Button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/Card'
import { formatDate, getSeverityColor, getStatusColor } from '../lib/utils'
import LoadingSpinner from './ui/LoadingSpinner'

interface AlertsPanelProps {
  open: boolean
  onClose: () => void
}

const AlertsPanel = ({ open, onClose }: AlertsPanelProps) => {
  const dispatch = useAppDispatch()
  const { alerts, activeAlerts, isLoading } = useAppSelector((state) => state.alerts)

  useEffect(() => {
    if (open) {
      dispatch(fetchAlerts({ status: 'active' }))
    }
  }, [open, dispatch])

  const handleAcknowledge = async (alertId: string) => {
    await dispatch(acknowledgeAlert(alertId))
  }

  const handleResolve = async (alertId: string) => {
    await dispatch(resolveAlert({ alertId }))
  }

  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-50"
            onClick={onClose}
          />

          {/* Panel */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed right-0 top-0 h-full w-96 bg-white dark:bg-gray-800 shadow-xl z-50 overflow-hidden"
          >
            <div className="flex flex-col h-full">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Active Alerts ({activeAlerts.length})
                </h2>
                <Button variant="ghost" size="icon" onClick={onClose}>
                  <X className="h-5 w-5" />
                </Button>
              </div>

              {/* Content */}
              <div className="flex-1 overflow-y-auto p-4">
                {isLoading ? (
                  <div className="flex items-center justify-center h-32">
                    <LoadingSpinner size="lg" />
                  </div>
                ) : activeAlerts.length === 0 ? (
                  <div className="text-center py-8">
                    <CheckCircle className="h-12 w-12 text-green-500 mx-auto mb-4" />
                    <p className="text-gray-500 dark:text-gray-400">
                      No active alerts
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {activeAlerts.map((alert) => (
                      <motion.div
                        key={alert.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="border rounded-lg p-4 bg-white dark:bg-gray-700 shadow-sm"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <AlertTriangle className="h-4 w-4 text-orange-500" />
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(alert.severity)}`}>
                              {alert.severity.toUpperCase()}
                            </span>
                          </div>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(alert.status)}`}>
                            {alert.status}
                          </span>
                        </div>

                        <h4 className="font-medium text-gray-900 dark:text-white mb-1">
                          {alert.alert_type}
                        </h4>
                        
                        <p className="text-sm text-gray-600 dark:text-gray-300 mb-2">
                          {alert.message}
                        </p>

                        <div className="text-xs text-gray-500 dark:text-gray-400 mb-3">
                          <div>Module: {alert.module}</div>
                          {alert.location && <div>Location: {alert.location}</div>}
                          <div className="flex items-center mt-1">
                            <Clock className="h-3 w-3 mr-1" />
                            {formatDate(alert.created_at)}
                          </div>
                        </div>

                        {alert.recommended_actions && alert.recommended_actions.length > 0 && (
                          <div className="mb-3">
                            <p className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                              Recommended Actions:
                            </p>
                            <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                              {alert.recommended_actions.map((action, index) => (
                                <li key={index} className="flex items-start">
                                  <span className="mr-1">•</span>
                                  <span>{action}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        <div className="flex space-x-2">
                          {alert.status === 'active' && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleAcknowledge(alert.id)}
                              className="flex-1"
                            >
                              Acknowledge
                            </Button>
                          )}
                          <Button
                            size="sm"
                            onClick={() => handleResolve(alert.id)}
                            className="flex-1"
                          >
                            Resolve
                          </Button>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                )}
              </div>

              {/* Footer */}
              <div className="p-4 border-t border-gray-200 dark:border-gray-700">
                <Button
                  variant="outline"
                  className="w-full"
                  onClick={() => {
                    onClose()
                    // Navigate to alerts page
                    window.location.href = '/alerts'
                  }}
                >
                  View All Alerts
                </Button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}

export default AlertsPanel
