import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { RootState } from '../store/store'
import LoadingSpinner from './LoadingSpinner'

interface PrivateRouteProps {
  children: React.ReactNode
}

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
  const location = useLocation()
  const { token, isLoading } = useSelector((state: RootState) => state.auth)

  // Show loading spinner while checking authentication
  if (isLoading) {
    return <LoadingSpinner />
  }

  // Redirect to login if not authenticated
  if (!token) {
    return <Navigate to="/auth/login" state={{ from: location }} replace />
  }

  // Render children if authenticated
  return <>{children}</>
}

export default PrivateRoute