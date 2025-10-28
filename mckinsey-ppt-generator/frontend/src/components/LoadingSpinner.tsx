import React from 'react'
import { Box, CircularProgress, Typography, Fade } from '@mui/material'

interface LoadingSpinnerProps {
  message?: string
  size?: number
  fullScreen?: boolean
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Loading...',
  size = 40,
  fullScreen = true,
}) => {
  const containerStyles = fullScreen
    ? {
        position: 'fixed' as const,
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        zIndex: 9999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }
    : {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '200px',
        width: '100%',
      }

  return (
    <Fade in={true} timeout={300}>
      <Box sx={containerStyles}>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            p: 3,
          }}
        >
          <CircularProgress
            size={size}
            thickness={4}
            sx={{
              color: 'primary.main',
              mb: 2,
            }}
          />
          {message && (
            <Typography
              variant="body1"
              color="text.secondary"
              sx={{
                fontWeight: 500,
                opacity: 0.8,
              }}
            >
              {message}
            </Typography>
          )}
        </Box>
      </Box>
    </Fade>
  )
}

export default LoadingSpinner