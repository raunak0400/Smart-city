import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  BarChart3, 
  TrendingUp, 
  Calendar, 
  Download,
  Filter,
  RefreshCw,
  Target,
  Activity,
  Users,
  Zap
} from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { analyticsAPI } from '../services/api'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card'
import { Button } from '../components/ui/Button'
import LoadingSpinner from '../components/ui/LoadingSpinner'
import { formatNumber } from '../lib/utils'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts'

const AnalyticsPage = () => {
  const [selectedTimeRange, setSelectedTimeRange] = useState('30d')
  const [selectedMetric, setSelectedMetric] = useState('all')

  // Fetch analytics data
  const { data: overview, isLoading: overviewLoading } = useQuery({
    queryKey: ['analytics-overview'],
    queryFn: analyticsAPI.getOverview,
    refetchInterval: 300000, // Refetch every 5 minutes
  })

  const { data: trafficPatterns } = useQuery({
    queryKey: ['traffic-patterns', selectedTimeRange],
    queryFn: () => analyticsAPI.getTrafficPatterns({ timeRange: selectedTimeRange }),
    refetchInterval: 600000, // Refetch every 10 minutes
  })

  const { data: kpiDashboard } = useQuery({
    queryKey: ['kpi-dashboard'],
    queryFn: analyticsAPI.getKPIDashboard,
    refetchInterval: 300000,
  })

  // Mock data for comprehensive analytics
  const cityPerformanceKPIs = [
    { metric: 'Traffic Efficiency', current: 87, target: 90, trend: '+2%' },
    { metric: 'Air Quality Index', current: 42, target: 50, trend: '-8%' },
    { metric: 'Waste Collection Rate', current: 94, target: 95, trend: '+1%' },
    { metric: 'Energy Efficiency', current: 91, target: 88, trend: '+5%' },
    { metric: 'Emergency Response', current: 96, target: 95, trend: '+3%' },
    { metric: 'Citizen Satisfaction', current: 78, target: 80, trend: '+4%' },
  ]

  const predictiveAnalytics = [
    { month: 'Jan', traffic: 85, energy: 92, waste: 88, environment: 76 },
    { month: 'Feb', traffic: 87, energy: 89, waste: 91, environment: 78 },
    { month: 'Mar', traffic: 89, energy: 94, waste: 89, environment: 82 },
    { month: 'Apr', traffic: 91, energy: 96, waste: 93, environment: 85 },
    { month: 'May', traffic: 88, energy: 91, waste: 95, environment: 87 },
    { month: 'Jun', traffic: 92, energy: 88, waste: 92, environment: 89 },
  ]

  const resourceOptimization = [
    { category: 'Traffic Signals', efficiency: 94, savings: '$125K', co2Reduced: '45 tons' },
    { category: 'Street Lighting', efficiency: 89, savings: '$89K', co2Reduced: '32 tons' },
    { category: 'Waste Routes', efficiency: 96, savings: '$156K', co2Reduced: '67 tons' },
    { category: 'Energy Grid', efficiency: 91, savings: '$234K', co2Reduced: '89 tons' },
  ]

  const citizenEngagement = [
    { platform: 'Mobile App', users: 45000, engagement: 78, satisfaction: 4.2 },
    { platform: 'Web Portal', users: 23000, engagement: 65, satisfaction: 3.9 },
    { platform: 'Social Media', users: 67000, engagement: 82, satisfaction: 4.1 },
    { platform: 'Call Center', users: 12000, engagement: 91, satisfaction: 4.5 },
  ]

  const performanceRadarData = [
    { subject: 'Traffic', A: 87, B: 90, fullMark: 100 },
    { subject: 'Environment', A: 76, B: 80, fullMark: 100 },
    { subject: 'Waste', A: 94, B: 95, fullMark: 100 },
    { subject: 'Energy', A: 91, B: 88, fullMark: 100 },
    { subject: 'Emergency', A: 96, B: 95, fullMark: 100 },
    { subject: 'Satisfaction', A: 78, B: 80, fullMark: 100 },
  ]

  const costBenefitAnalysis = [
    { name: 'Smart Traffic', investment: 2.5, savings: 4.2, roi: 168 },
    { name: 'Air Quality Monitoring', investment: 1.8, savings: 2.1, roi: 117 },
    { name: 'Waste Optimization', investment: 3.2, savings: 5.8, roi: 181 },
    { name: 'Energy Management', investment: 4.1, savings: 7.3, roi: 178 },
    { name: 'Emergency Systems', investment: 2.9, savings: 3.8, roi: 131 },
  ]

  const exportReport = async (type: string) => {
    try {
      const response = await analyticsAPI.getComprehensiveReports({ 
        format: type,
        timeRange: selectedTimeRange 
      })
      // Handle file download
      console.log('Exporting report:', type)
    } catch (error) {
      console.error('Failed to export report:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Analytics & Reports
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Comprehensive city performance analytics and predictive insights
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => exportReport('pdf')}>
            <Download className="h-4 w-4 mr-2" />
            Export PDF
          </Button>
          <Button variant="outline" onClick={() => exportReport('csv')}>
            <Download className="h-4 w-4 mr-2" />
            Export CSV
          </Button>
          <select
            value={selectedTimeRange}
            onChange={(e) => setSelectedTimeRange(e.target.value)}
            className="border rounded-md px-3 py-2 text-sm"
          >
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
            <option value="1y">Last Year</option>
          </select>
        </div>
      </div>

      {/* KPI Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {cityPerformanceKPIs.map((kpi, index) => (
          <motion.div
            key={kpi.metric}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    {kpi.metric}
                  </h4>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    kpi.trend.startsWith('+') ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                  }`}>
                    {kpi.trend}
                  </span>
                </div>
                <div className="flex items-end justify-between">
                  <div>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">
                      {kpi.current}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      Target: {kpi.target}
                    </p>
                  </div>
                  <div className="w-16 h-16">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={[
                            { value: kpi.current, fill: kpi.current >= kpi.target ? '#10b981' : '#f59e0b' },
                            { value: 100 - kpi.current, fill: '#e5e7eb' }
                          ]}
                          cx="50%"
                          cy="50%"
                          innerRadius={12}
                          outerRadius={24}
                          startAngle={90}
                          endAngle={450}
                          dataKey="value"
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Performance Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* City Performance Radar */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Target className="h-5 w-5 mr-2" />
              City Performance Overview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={performanceRadarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" />
                <PolarRadiusAxis angle={30} domain={[0, 100]} />
                <Radar
                  name="Current"
                  dataKey="A"
                  stroke="#3b82f6"
                  fill="#3b82f6"
                  fillOpacity={0.3}
                />
                <Radar
                  name="Target"
                  dataKey="B"
                  stroke="#10b981"
                  fill="#10b981"
                  fillOpacity={0.3}
                />
                <Legend />
              </RadarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Predictive Analytics */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2" />
              Predictive Performance Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={predictiveAnalytics}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="traffic" stroke="#3b82f6" strokeWidth={2} name="Traffic" />
                <Line type="monotone" dataKey="energy" stroke="#10b981" strokeWidth={2} name="Energy" />
                <Line type="monotone" dataKey="waste" stroke="#f59e0b" strokeWidth={2} name="Waste" />
                <Line type="monotone" dataKey="environment" stroke="#ef4444" strokeWidth={2} name="Environment" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Resource Optimization */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Activity className="h-5 w-5 mr-2" />
            Resource Optimization Impact
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {resourceOptimization.map((resource) => (
              <div key={resource.category} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                  {resource.category}
                </h4>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Efficiency</span>
                    <span className="font-medium text-gray-900 dark:text-white">{resource.efficiency}%</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Savings</span>
                    <span className="font-medium text-green-600">{resource.savings}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">CO₂ Reduced</span>
                    <span className="font-medium text-blue-600">{resource.co2Reduced}</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                    <div 
                      className="bg-green-500 h-2 rounded-full" 
                      style={{ width: `${resource.efficiency}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Citizen Engagement and Cost-Benefit Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Citizen Engagement */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Users className="h-5 w-5 mr-2" />
              Citizen Engagement Analytics
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {citizenEngagement.map((platform) => (
                <div key={platform.platform} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900 dark:text-white">
                      {platform.platform}
                    </h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {formatNumber(platform.users)} users
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {platform.engagement}% engagement
                    </p>
                    <div className="flex items-center">
                      <span className="text-xs text-gray-500 dark:text-gray-400 mr-1">★</span>
                      <span className="text-xs text-gray-600 dark:text-gray-300">
                        {platform.satisfaction}/5.0
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Cost-Benefit Analysis */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <BarChart3 className="h-5 w-5 mr-2" />
              ROI Analysis by System
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={costBenefitAnalysis}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="roi" fill="#10b981" name="ROI %" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Metrics Table */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              Detailed Performance Metrics
            </div>
            <div className="flex space-x-2">
              <Button variant="outline" size="sm">
                <Filter className="h-4 w-4 mr-2" />
                Filter
              </Button>
              <Button variant="outline" size="sm">
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh
              </Button>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Metric</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Current</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Target</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Trend</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Status</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-900 dark:text-white">Last Updated</th>
                </tr>
              </thead>
              <tbody>
                {cityPerformanceKPIs.map((kpi, index) => (
                  <tr key={index} className="border-b border-gray-100 dark:border-gray-800">
                    <td className="py-3 px-4 text-gray-900 dark:text-white">{kpi.metric}</td>
                    <td className="py-3 px-4 text-gray-900 dark:text-white font-medium">{kpi.current}</td>
                    <td className="py-3 px-4 text-gray-600 dark:text-gray-400">{kpi.target}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        kpi.trend.startsWith('+') ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                      }`}>
                        {kpi.trend}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs ${
                        kpi.current >= kpi.target ? 'bg-green-100 text-green-600' : 'bg-yellow-100 text-yellow-600'
                      }`}>
                        {kpi.current >= kpi.target ? 'On Target' : 'Below Target'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-gray-500 dark:text-gray-400">2 min ago</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* System Health Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { system: 'Traffic Management', health: 94, alerts: 2, uptime: '99.8%' },
          { system: 'Environmental Monitoring', health: 87, alerts: 5, uptime: '99.2%' },
          { system: 'Waste Management', health: 96, alerts: 1, uptime: '99.9%' },
          { system: 'Energy Grid', health: 91, alerts: 3, uptime: '99.5%' },
        ].map((system) => (
          <Card key={system.system}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-sm font-medium text-gray-900 dark:text-white">
                  {system.system}
                </h4>
                <Zap className={`h-4 w-4 ${
                  system.health >= 95 ? 'text-green-500' :
                  system.health >= 85 ? 'text-yellow-500' : 'text-red-500'
                }`} />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-xs text-gray-600 dark:text-gray-400">Health Score</span>
                  <span className="text-xs font-medium text-gray-900 dark:text-white">{system.health}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-xs text-gray-600 dark:text-gray-400">Active Alerts</span>
                  <span className="text-xs font-medium text-gray-900 dark:text-white">{system.alerts}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-xs text-gray-600 dark:text-gray-400">Uptime</span>
                  <span className="text-xs font-medium text-gray-900 dark:text-white">{system.uptime}</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-1.5">
                  <div 
                    className={`h-1.5 rounded-full ${
                      system.health >= 95 ? 'bg-green-500' :
                      system.health >= 85 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${system.health}%` }}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}

export default AnalyticsPage
