import React, { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { Container, Box } from '@mui/material'

import { AppDispatch } from './store/store'
import { initializeAuth } from './store/authSlice'

// Layout components
import Navbar from './components/Navbar'
import PrivateRoute from './components/PrivateRoute'

// Auth pages
import AuthLayout from './pages/auth/AuthLayout'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'

// Dashboard pages
import Dashboard from './pages/dashboard/Dashboard'
import PresentationList from './pages/dashboard/PresentationList'
import CreatePresentation from './pages/dashboard/CreatePresentation'
import PresentationEditor from './pages/dashboard/PresentationEditor'

function App() {
  const dispatch = useDispatch<AppDispatch>()

  useEffect(() => {
    // Initialize authentication state from localStorage
    dispatch(initializeAuth())
  }, [dispatch])

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: 'background.default' }}>
      <Routes>
        {/* Auth routes */}
        <Route path="/auth" element={<AuthLayout />}>
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
        </Route>

        {/* Protected routes */}
        <Route
          path="/*"
          element={
            <PrivateRoute>
              <Navbar />
              <Container maxWidth="xl" sx={{ py: 3 }}>
                <Routes>
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/presentations" element={<PresentationList />} />
                  <Route path="/presentations/new" element={<CreatePresentation />} />
                  <Route path="/presentations/:id/edit" element={<PresentationEditor />} />
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </Container>
            </PrivateRoute>
          }
        />

        {/* Default redirect */}
        <Route path="*" element={<Navigate to="/auth/login" replace />} />
      </Routes>
    </Box>
  )
}

export default App