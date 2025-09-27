import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { alertsAPI } from '../services/api'

export interface Alert {
  id: string
  alert_type: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  message: string
  module: string
  status: 'active' | 'acknowledged' | 'resolved'
  created_at: string
  acknowledged_at?: string
  resolved_at?: string
  location?: string
  affected_systems?: string[]
  recommended_actions?: string[]
}

interface AlertsState {
  alerts: Alert[]
  activeAlerts: Alert[]
  isLoading: boolean
  error: string | null
  filters: {
    status: string
    severity: string
    module: string
  }
}

const initialState: AlertsState = {
  alerts: [],
  activeAlerts: [],
  isLoading: false,
  error: null,
  filters: {
    status: 'active',
    severity: '',
    module: '',
  },
}

export const fetchAlerts = createAsyncThunk(
  'alerts/fetchAlerts',
  async (filters?: Partial<AlertsState['filters']>, { rejectWithValue }) => {
    try {
      const response = await alertsAPI.getAlerts(filters)
      return response.alerts
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch alerts')
    }
  }
)

export const acknowledgeAlert = createAsyncThunk(
  'alerts/acknowledgeAlert',
  async (alertId: string, { rejectWithValue }) => {
    try {
      await alertsAPI.acknowledgeAlert(alertId)
      return alertId
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to acknowledge alert')
    }
  }
)

export const resolveAlert = createAsyncThunk(
  'alerts/resolveAlert',
  async ({ alertId, notes }: { alertId: string; notes?: string }, { rejectWithValue }) => {
    try {
      await alertsAPI.resolveAlert(alertId, notes)
      return alertId
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to resolve alert')
    }
  }
)

const alertsSlice = createSlice({
  name: 'alerts',
  initialState,
  reducers: {
    addAlert: (state, action) => {
      state.alerts.unshift(action.payload)
      if (action.payload.status === 'active') {
        state.activeAlerts.unshift(action.payload)
      }
    },
    updateAlert: (state, action) => {
      const index = state.alerts.findIndex(alert => alert.id === action.payload.id)
      if (index !== -1) {
        state.alerts[index] = { ...state.alerts[index], ...action.payload }
      }
      
      const activeIndex = state.activeAlerts.findIndex(alert => alert.id === action.payload.id)
      if (activeIndex !== -1) {
        if (action.payload.status === 'active') {
          state.activeAlerts[activeIndex] = { ...state.activeAlerts[activeIndex], ...action.payload }
        } else {
          state.activeAlerts.splice(activeIndex, 1)
        }
      }
    },
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload }
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Alerts
      .addCase(fetchAlerts.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchAlerts.fulfilled, (state, action) => {
        state.isLoading = false
        state.alerts = action.payload
        state.activeAlerts = action.payload.filter(alert => alert.status === 'active')
      })
      .addCase(fetchAlerts.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      // Acknowledge Alert
      .addCase(acknowledgeAlert.fulfilled, (state, action) => {
        const alertId = action.payload
        const alert = state.alerts.find(a => a.id === alertId)
        if (alert) {
          alert.status = 'acknowledged'
          alert.acknowledged_at = new Date().toISOString()
        }
        state.activeAlerts = state.activeAlerts.filter(a => a.id !== alertId)
      })
      // Resolve Alert
      .addCase(resolveAlert.fulfilled, (state, action) => {
        const alertId = action.payload
        const alert = state.alerts.find(a => a.id === alertId)
        if (alert) {
          alert.status = 'resolved'
          alert.resolved_at = new Date().toISOString()
        }
        state.activeAlerts = state.activeAlerts.filter(a => a.id !== alertId)
      })
  },
})

export const { addAlert, updateAlert, setFilters, clearError } = alertsSlice.actions
export default alertsSlice.reducer
