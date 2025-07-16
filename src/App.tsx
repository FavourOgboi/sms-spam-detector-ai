import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import Layout from './components/layout/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import Contact from './pages/Contact';
import Dashboard from './pages/Dashboard';
import Explanation from './pages/Explanation';
import History from './pages/History';
import Login from './pages/Login';
import Predict from './pages/Predict';
import Profile from './pages/Profile';
import Register from './pages/Register';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Protected Routes */}
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="predict" element={<Predict />} />
              <Route path="history" element={<History />} />
              <Route path="explanation" element={<Explanation />} />
              <Route path="profile" element={<Profile />} />
              <Route path="contact" element={<Contact />} />
            </Route>
            
            {/* Catch all route */}
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;