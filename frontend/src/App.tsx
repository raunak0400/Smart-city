import { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from './hooks/redux'
import { checkAuth } from './store/authSlice'
import { ThemeProvider } from './components/ThemeProvider'
import AuthLayout from './layouts/AuthLayout'
import DashboardLayout from './layouts/DashboardLayout'
import LoginPage from './pages/auth/LoginPage'
import DashboardPage from './pages/DashboardPage'
import TrafficPage from './pages/TrafficPage'
import EnvironmentPage from './pages/EnvironmentPage'
import WastePage from './pages/WastePage'
import EnergyPage from './pages/EnergyPage'
import EmergencyPage from './pages/EmergencyPage'
import AnalyticsPage from './pages/AnalyticsPage'
import AlertsPage from './pages/AlertsPage'
import ProfilePage from './pages/ProfilePage'
import LoadingSpinner from './components/ui/LoadingSpinner'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  const dispatch = useAppDispatch()
  const { isAuthenticated, isLoading } = useAppSelector((state) => state.auth)

  useEffect(() => {
    dispatch(checkAuth())
  }, [dispatch])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <ThemeProvider defaultTheme="light" storageKey="smart-city-theme">
      <Routes>
        {/* Public Routes */}
        <Route path="/auth" element={<AuthLayout />}>
          <Route path="login" element={<LoginPage />} />
          <Route index element={<Navigate to="login" replace />} />
        </Route>

        {/* Protected Routes */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<DashboardPage />} />
          <Route path="traffic" element={<TrafficPage />} />
          <Route path="environment" element={<EnvironmentPage />} />
          <Route path="waste" element={<WastePage />} />
          <Route path="energy" element={<EnergyPage />} />
          <Route path="emergency" element={<EmergencyPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="alerts" element={<AlertsPage />} />
          <Route path="profile" element={<ProfilePage />} />
        </Route>

        {/* Redirect unauthenticated users to login */}
        <Route
          path="*"
          element={
            isAuthenticated ? (
              <Navigate to="/" replace />
            ) : (
              <Navigate to="/auth/login" replace />
            )
          }
        />
      </Routes>
    </ThemeProvider>
  )
}

export default App
