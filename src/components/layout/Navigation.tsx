import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LayoutDashboard, 
  MessageSquare, 
  History, 
  Info, 
  User, 
  LogOut, 
  Menu, 
  X,
  Shield,
  Sun,
  Moon,
  MessageCircle
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import Modal from '../ui/Modal';

// Helper function to get user initials
const getUserInitials = (username: string, email: string) => {
  if (username && username.trim()) {
    return username.charAt(0).toUpperCase();
  }
  if (email && email.trim()) {
    return email.charAt(0).toUpperCase();
  }
  return 'U';
};

// Helper function to determine profile image source
const getProfileImageSrc = (user: any) => {
  // If user has uploaded a profile image, use it
  if (user?.profileImage && user.profileImage !== '/pres.jpg') {
    return user.profileImage;
  }
  // Otherwise return null to show initials
  return null;
};

const Navigation: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [logoutModalOpen, setLogoutModalOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const navigationItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Predict', path: '/predict', icon: MessageSquare },
    { name: 'History', path: '/history', icon: History },
    { name: 'Explanation', path: '/explanation', icon: Info },
    { name: 'Profile', path: '/profile', icon: User },
    { name: 'Contact', path: '/contact', icon: MessageCircle },
  ];

  const handleLogout = () => {
    setLogoutModalOpen(true);
  };

  const confirmLogout = () => {
    logout();
    navigate('/login');
    setLogoutModalOpen(false);
    setIsMobileMenuOpen(false);
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <>
      {/* Desktop Sidebar */}
      <div className="hidden md:flex fixed inset-y-0 left-0 z-50 w-64 bg-navy-900 dark:bg-gray-900 shadow-xl">
        <div className="flex flex-col w-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-16 px-4 bg-navy-800 dark:bg-gray-800">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <Shield className="h-8 w-8 text-accent-500" />
              <span className="text-xl font-bold text-white">SMS Guard</span>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {navigationItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                  isActive(item.path)
                    ? 'bg-primary-500 text-white shadow-lg'
                    : 'text-gray-300 hover:bg-navy-700 dark:hover:bg-gray-700 hover:text-white'
                }`}
              >
                <item.icon className="h-5 w-5" />
                <span className="font-medium">{item.name}</span>
              </Link>
            ))}
          </nav>

          {/* Theme Toggle */}
          <div className="px-4 py-2">
            <button
              onClick={toggleTheme}
              className="flex items-center space-x-3 w-full px-4 py-3 text-gray-300 hover:bg-navy-700 dark:hover:bg-gray-700 hover:text-white rounded-lg transition-all duration-200"
            >
              {theme === 'light' ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}
              <span className="font-medium">{theme === 'light' ? 'Dark Mode' : 'Light Mode'}</span>
            </button>
          </div>

          {/* User Profile & Logout */}
          <div className="border-t border-navy-700 dark:border-gray-700 p-4">
            {/* Creator Information */}
            <div className="mb-4 p-3 bg-navy-800 dark:bg-gray-700 rounded-lg">
              <p className="text-xs text-gray-400 text-center leading-relaxed">
                Created by <span className="text-white font-medium">Ogboi Favour Ifeanyichukwu</span>, Computer Science Graduate from Federal University of Petroleum Resources Effurun
              </p>
            </div>
            
            <div className="flex items-center space-x-3 mb-4">
              {getProfileImageSrc(user) ? (
                <img
                  src={getProfileImageSrc(user)!}
                  alt={user?.username || 'User'}
                  className="h-10 w-10 rounded-full object-cover"
                />
              ) : (
                <div className="h-10 w-10 rounded-full bg-primary-500 flex items-center justify-center">
                  <span className="text-sm font-bold text-white">
                    {getUserInitials(user?.username || '', user?.email || '')}
                  </span>
                </div>
              )}
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">
                  {user?.username || 'User'}
                </p>
                <p className="text-xs text-gray-400 truncate">
                  {user?.email || 'user@example.com'}
                </p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center space-x-2 w-full px-4 py-2 text-sm text-gray-300 hover:bg-navy-700 dark:hover:bg-gray-700 hover:text-white rounded-lg transition-all duration-200"
            >
              <LogOut className="h-4 w-4" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Header */}
      <div className="md:hidden bg-navy-900 dark:bg-gray-900 shadow-lg">
        <div className="flex items-center justify-between px-4 py-3">
          <Link to="/dashboard" className="flex items-center space-x-2">
            <Shield className="h-7 w-7 text-accent-500" />
            <span className="text-lg font-bold text-white">SMS Guard</span>
          </Link>
          <div className="flex items-center space-x-2">
            <button
              onClick={toggleTheme}
              className="p-2 text-gray-300 hover:text-white transition-colors"
            >
              {theme === 'light' ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}
            </button>
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="p-2 text-gray-300 hover:text-white transition-colors"
            >
              {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.2 }}
            className="md:hidden bg-navy-800 dark:bg-gray-800 shadow-lg"
          >
            <nav className="px-4 py-2 space-y-1">
              {navigationItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                    isActive(item.path)
                      ? 'bg-primary-500 text-white'
                      : 'text-gray-300 hover:bg-navy-700 dark:hover:bg-gray-700 hover:text-white'
                  }`}
                >
                  <item.icon className="h-5 w-5" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              ))}
              <button
                onClick={handleLogout}
                className="flex items-center space-x-3 w-full px-4 py-3 text-gray-300 hover:bg-navy-700 dark:hover:bg-gray-700 hover:text-white rounded-lg transition-all duration-200"
              >
                <LogOut className="h-5 w-5" />
                <span className="font-medium">Logout</span>
              </button>
            </nav>
            
            {/* Creator Information for Mobile */}
            <div className="px-4 py-3 border-t border-navy-700 dark:border-gray-700">
              <p className="text-xs text-gray-400 text-center leading-relaxed">
                Created by <span className="text-white font-medium">Ogboi Favour Ifeanyichukwu</span>, Computer Science Graduate from Federal University of Petroleum Resources Effurun
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Logout Confirmation Modal */}
      <Modal
        isOpen={logoutModalOpen}
        onClose={() => setLogoutModalOpen(false)}
        title="Confirm Logout"
      >
        <div className="space-y-4">
          <p className="text-gray-700 dark:text-gray-300">
            Are you sure you want to logout? You'll need to sign in again to access your account.
          </p>
          
          <div className="flex space-x-3 pt-4">
            <button
              onClick={() => setLogoutModalOpen(false)}
              className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 rounded-lg font-medium hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={confirmLogout}
              className="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg font-medium hover:bg-red-600 transition-colors"
            >
              <div className="flex items-center justify-center">
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </div>
            </button>
          </div>
        </div>
      </Modal>
    </>
  );
};

export default Navigation;