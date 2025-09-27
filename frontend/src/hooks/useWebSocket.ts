import { useEffect, useRef } from 'react'
import { io, Socket } from 'socket.io-client'
import { useAppDispatch, useAppSelector } from './redux'
import { addAlert, updateAlert } from '../store/alertsSlice'
import { updateRealTimeData } from '../store/dashboardSlice'
import toast from 'react-hot-toast'

export const useWebSocket = () => {
  const socketRef = useRef<Socket | null>(null)
  const dispatch = useAppDispatch()
  const { isAuthenticated, token } = useAppSelector((state) => state.auth)

  useEffect(() => {
    if (!isAuthenticated || !token) {
      return
    }

    // Initialize socket connection
    const socket = io('http://localhost:5000', {
      auth: {
        token: token
      },
      transports: ['websocket', 'polling']
    })

    socketRef.current = socket

    // Connection events
    socket.on('connect', () => {
      console.log('Connected to WebSocket server')
      
      // Join relevant rooms
      socket.emit('join_room', { room: 'alerts' })
      socket.emit('join_room', { room: 'dashboard' })
      socket.emit('subscribe_alerts', { 
        severity_levels: ['high', 'critical'],
        modules: ['traffic', 'environment', 'waste', 'energy', 'emergency'] 
      })
    })

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server')
    })

    socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error)
    })

    // Alert events
    socket.on('new_alert', (data) => {
      dispatch(addAlert(data.alert))
      
      // Show toast notification for high/critical alerts
      if (['high', 'critical'].includes(data.alert.severity)) {
        toast.error(`${data.alert.severity.toUpperCase()}: ${data.alert.message}`, {
          duration: 6000,
          icon: '🚨'
        })
      }
    })

    socket.on('alert_acknowledged', (data) => {
      dispatch(updateAlert({
        id: data.alert_id,
        status: 'acknowledged',
        acknowledged_at: data.acknowledged_at,
        acknowledged_by: data.acknowledged_by
      }))
    })

    socket.on('alert_resolved', (data) => {
      dispatch(updateAlert({
        id: data.alert_id,
        status: 'resolved',
        resolved_at: data.resolved_at,
        resolved_by: data.resolved_by
      }))
    })

    socket.on('alerts_bulk_acknowledged', (data) => {
      data.alert_ids.forEach((alertId: string) => {
        dispatch(updateAlert({
          id: alertId,
          status: 'acknowledged',
          acknowledged_at: new Date().toISOString(),
          acknowledged_by: data.acknowledged_by
        }))
      })
      
      toast.success(`${data.count} alerts acknowledged`)
    })

    // Real-time data updates
    socket.on('traffic_update', (data) => {
      dispatch(updateRealTimeData({ traffic: data }))
    })

    socket.on('environment_update', (data) => {
      dispatch(updateRealTimeData({ environment: data }))
    })

    socket.on('waste_update', (data) => {
      dispatch(updateRealTimeData({ waste: data }))
    })

    socket.on('energy_update', (data) => {
      dispatch(updateRealTimeData({ energy: data }))
    })

    socket.on('emergency_alert', (incident) => {
      toast.error(`EMERGENCY: ${incident.type} - ${incident.location}`, {
        duration: 10000,
        icon: '🚨'
      })
    })

    socket.on('system_update', (update) => {
      if (update.type === 'maintenance') {
        toast(`System Maintenance: ${update.message}`, {
          icon: '🔧'
        })
      } else if (update.type === 'warning') {
        toast.error(`System Warning: ${update.message}`)
      }
    })

    // Cleanup on unmount
    return () => {
      socket.disconnect()
      socketRef.current = null
    }
  }, [isAuthenticated, token, dispatch])

  // Function to emit events
  const emitEvent = (event: string, data: any) => {
    if (socketRef.current?.connected) {
      socketRef.current.emit(event, data)
    }
  }

  return {
    socket: socketRef.current,
    emitEvent,
    isConnected: socketRef.current?.connected || false
  }
}
