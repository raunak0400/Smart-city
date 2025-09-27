import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/auth/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: async (credentials: { email: string; password: string }) => {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },
  
  getProfile: async () => {
    const response = await api.get('/auth/profile')
    return response.data
  },
  
  updateProfile: async (profileData: any) => {
    const response = await api.put('/auth/profile', profileData)
    return response.data
  },
  
  changePassword: async (passwordData: { current_password: string; new_password: string }) => {
    const response = await api.post('/auth/change-password', passwordData)
    return response.data
  },
}

// Dashboard API
export const dashboardAPI = {
  getOverview: async () => {
    const response = await api.get('/dashboard/overview')
    return response.data
  },
  
  getRealTimeData: async () => {
    const response = await api.get('/dashboard/real-time-data')
    return response.data
  },
  
  getAlertsummary: async () => {
    const response = await api.get('/dashboard/alerts/summary')
    return response.data
  },
  
  getWeeklyStatistics: async () => {
    const response = await api.get('/dashboard/statistics/weekly')
    return response.data
  },
}

// Traffic API
export const trafficAPI = {
  getTrafficData: async (params?: any) => {
    const response = await api.get('/traffic/data', { params })
    return response.data
  },
  
  addTrafficData: async (data: any) => {
    const response = await api.post('/traffic/data', data)
    return response.data
  },
  
  getIncidents: async (params?: any) => {
    const response = await api.get('/traffic/incidents', { params })
    return response.data
  },
  
  reportIncident: async (incident: any) => {
    const response = await api.post('/traffic/incidents', incident)
    return response.data
  },
  
  optimizeSignals: async (data: any) => {
    const response = await api.get('/traffic/optimization/signals', { params: data })
    return response.data
  },
  
  optimizeRoutes: async (data: any) => {
    const response = await api.post('/traffic/optimization/routes', data)
    return response.data
  },
}

// Environment API
export const environmentAPI = {
  getEnvironmentData: async (params?: any) => {
    const response = await api.get('/environment/data', { params })
    return response.data
  },
  
  addSensorData: async (data: any) => {
    const response = await api.post('/environment/data', data)
    return response.data
  },
  
  getAirQualitySummary: async () => {
    const response = await api.get('/environment/air-quality/summary')
    return response.data
  },
  
  getPollutionTrends: async (params?: any) => {
    const response = await api.get('/environment/pollution/trends', { params })
    return response.data
  },
  
  getEnvironmentAlerts: async () => {
    const response = await api.get('/environment/alerts')
    return response.data
  },
}

// Waste API
export const wasteAPI = {
  getBins: async (params?: any) => {
    const response = await api.get('/waste/bins', { params })
    return response.data
  },
  
  addBin: async (bin: any) => {
    const response = await api.post('/waste/bins', bin)
    return response.data
  },
  
  updateBinLevel: async (binId: string, level: number) => {
    const response = await api.put(`/waste/bins/${binId}/update-level`, { level })
    return response.data
  },
  
  getCollections: async (params?: any) => {
    const response = await api.get('/waste/collections', { params })
    return response.data
  },
  
  scheduleCollection: async (collection: any) => {
    const response = await api.post('/waste/collections', collection)
    return response.data
  },
  
  optimizeRoutes: async (data: any) => {
    const response = await api.post('/waste/optimization/routes', data)
    return response.data
  },
}

// Energy API
export const energyAPI = {
  getGrids: async (params?: any) => {
    const response = await api.get('/energy/grids', { params })
    return response.data
  },
  
  addGridData: async (data: any) => {
    const response = await api.post('/energy/grids', data)
    return response.data
  },
  
  getConsumption: async (params?: any) => {
    const response = await api.get('/energy/consumption', { params })
    return response.data
  },
  
  getRenewableData: async (params?: any) => {
    const response = await api.get('/energy/renewable', { params })
    return response.data
  },
  
  optimizeLoadBalancing: async (data: any) => {
    const response = await api.get('/energy/optimization/load-balancing', { params: data })
    return response.data
  },
}

// Emergency API
export const emergencyAPI = {
  getIncidents: async (params?: any) => {
    const response = await api.get('/emergency/incidents', { params })
    return response.data
  },
  
  createIncident: async (incident: any) => {
    const response = await api.post('/emergency/incidents', incident)
    return response.data
  },
  
  getUnits: async (params?: any) => {
    const response = await api.get('/emergency/units', { params })
    return response.data
  },
  
  dispatchUnit: async (unitId: string, incidentId: string) => {
    const response = await api.post(`/emergency/units/${unitId}/dispatch`, { incident_id: incidentId })
    return response.data
  },
  
  broadcastAlert: async (alert: any) => {
    const response = await api.post('/emergency/alerts/broadcast', alert)
    return response.data
  },
}

// Analytics API
export const analyticsAPI = {
  getOverview: async () => {
    const response = await api.get('/analytics/overview')
    return response.data
  },
  
  getTrafficPatterns: async (params?: any) => {
    const response = await api.get('/analytics/traffic/patterns', { params })
    return response.data
  },
  
  getPredictiveTraffic: async (params?: any) => {
    const response = await api.get('/analytics/predictive/traffic', { params })
    return response.data
  },
  
  getKPIDashboard: async () => {
    const response = await api.get('/analytics/kpi/dashboard')
    return response.data
  },
  
  getComprehensiveReports: async (params?: any) => {
    const response = await api.get('/analytics/reports/comprehensive', { params })
    return response.data
  },
}

// Alerts API
export const alertsAPI = {
  getAlerts: async (filters?: any) => {
    const response = await api.get('/alerts', { params: filters })
    return response.data
  },
  
  createAlert: async (alert: any) => {
    const response = await api.post('/alerts', alert)
    return response.data
  },
  
  acknowledgeAlert: async (alertId: string) => {
    const response = await api.put(`/alerts/${alertId}/acknowledge`)
    return response.data
  },
  
  resolveAlert: async (alertId: string, notes?: string) => {
    const response = await api.put(`/alerts/${alertId}/resolve`, { resolution_notes: notes })
    return response.data
  },
  
  bulkAcknowledge: async (alertIds: string[]) => {
    const response = await api.put('/alerts/bulk-acknowledge', { alert_ids: alertIds })
    return response.data
  },
  
  getStatistics: async (days?: number) => {
    const response = await api.get('/alerts/statistics', { params: { days } })
    return response.data
  },
  
  getNotificationSettings: async () => {
    const response = await api.get('/alerts/notifications/settings')
    return response.data
  },
  
  updateNotificationSettings: async (settings: any) => {
    const response = await api.put('/alerts/notifications/settings', settings)
    return response.data
  },
}

export default api
