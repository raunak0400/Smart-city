import { Outlet } from 'react-router-dom'
import { motion } from 'framer-motion'

const AuthLayout = () => {
  return (
    <div className="min-h-screen flex">
      {/* Left side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-blue-600 to-purple-700 relative overflow-hidden">
        <div className="absolute inset-0 bg-black/20" />
        <div className="relative z-10 flex flex-col justify-center items-center text-white p-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 className="text-4xl font-bold mb-4">Smart City Management</h1>
            <p className="text-xl mb-8 opacity-90">
              Comprehensive city infrastructure monitoring and management platform
            </p>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
                <h3 className="font-semibold mb-2">Traffic Management</h3>
                <p className="opacity-80">Real-time monitoring and optimization</p>
              </div>
              <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
                <h3 className="font-semibold mb-2">Environmental Monitoring</h3>
                <p className="opacity-80">Air quality and pollution tracking</p>
              </div>
              <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
                <h3 className="font-semibold mb-2">Waste Management</h3>
                <p className="opacity-80">Smart bin monitoring and routing</p>
              </div>
              <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
                <h3 className="font-semibold mb-2">Energy Management</h3>
                <p className="opacity-80">Grid monitoring and optimization</p>
              </div>
            </div>
          </motion.div>
        </div>
        
        {/* Animated background elements */}
        <div className="absolute top-10 left-10 w-20 h-20 bg-white/10 rounded-full animate-pulse" />
        <div className="absolute bottom-20 right-20 w-32 h-32 bg-white/5 rounded-full animate-pulse delay-1000" />
        <div className="absolute top-1/2 right-10 w-16 h-16 bg-white/10 rounded-full animate-pulse delay-500" />
      </div>

      {/* Right side - Auth Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-gray-50 dark:bg-gray-900">
        <div className="w-full max-w-md">
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Outlet />
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default AuthLayout
