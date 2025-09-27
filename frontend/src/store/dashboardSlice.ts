import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { dashboardAPI } from '../services/api'

interface DashboardStats {
  totalAlerts: number
  activeIncidents: number
  trafficFlow: number
  energyConsumption: number
  wasteLevel: number
  airQuality: number
}

interface DashboardState {
  stats: DashboardStats | null
  realTimeData: any
  isLoading: boolean
  error: string | null
  lastUpdated: string | null
}

const initialState: DashboardState = {
  stats: null,
  realTimeData: null,
  isLoading: false,
  error: null,
  lastUpdated: null,
}

export const fetchDashboardOverview = createAsyncThunk(
  'dashboard/fetchOverview',
  async (_, { rejectWithValue }) => {
    try {
      const response = await dashboardAPI.getOverview()
      return response
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch dashboard data')
    }
  }
)

export const fetchRealTimeData = createAsyncThunk(
  'dashboard/fetchRealTimeData',
  async (_, { rejectWithValue }) => {
    try {
      const response = await dashboardAPI.getRealTimeData()
      return response
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch real-time data')
    }
  }
)

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {
    updateRealTimeData: (state, action) => {
      state.realTimeData = { ...state.realTimeData, ...action.payload }
      state.lastUpdated = new Date().toISOString()
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Overview
      .addCase(fetchDashboardOverview.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchDashboardOverview.fulfilled, (state, action) => {
        state.isLoading = false
        state.stats = action.payload
        state.lastUpdated = new Date().toISOString()
      })
      .addCase(fetchDashboardOverview.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      // Fetch Real-time Data
      .addCase(fetchRealTimeData.fulfilled, (state, action) => {
        state.realTimeData = action.payload
        state.lastUpdated = new Date().toISOString()
      })
  },
})

export const { updateRealTimeData, clearError } = dashboardSlice.actions
export default dashboardSlice.reducer
