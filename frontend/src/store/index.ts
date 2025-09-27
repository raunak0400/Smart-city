import { configureStore } from '@reduxjs/toolkit'
import authSlice from './authSlice'
import dashboardSlice from './dashboardSlice'
import alertsSlice from './alertsSlice'

export const store = configureStore({
  reducer: {
    auth: authSlice,
    dashboard: dashboardSlice,
    alerts: alertsSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
