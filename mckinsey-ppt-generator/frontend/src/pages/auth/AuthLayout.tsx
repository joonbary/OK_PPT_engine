import React from 'react'
import { Outlet, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { Box, Container, Paper, Typography, Grid } from '@mui/material'
import { RootState } from '../../store/store'

const AuthLayout: React.FC = () => {
  const { token } = useSelector((state: RootState) => state.auth)

  // Redirect to dashboard if already authenticated
  if (token) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        backgroundColor: 'background.default',
        backgroundImage: `linear-gradient(135deg, #0070C0 0%, #002E6C 100%)`,
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={0} sx={{ minHeight: '80vh' }}>
          {/* Left side - Branding */}
          <Grid
            item
            xs={12}
            md={6}
            sx={{
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              color: 'white',
              p: 4,
            }}
          >
            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Typography
                variant="h2"
                component="h1"
                sx={{
                  fontWeight: 700,
                  fontSize: { xs: '2.5rem', md: '3.5rem' },
                  mb: 2,
                  textShadow: '0 2px 4px rgba(0,0,0,0.3)',
                }}
              >
                McKinsey
              </Typography>
              <Typography
                variant="h4"
                component="h2"
                sx={{
                  fontWeight: 500,
                  fontSize: { xs: '1.5rem', md: '2rem' },
                  mb: 3,
                  opacity: 0.9,
                }}
              >
                PPT Generator
              </Typography>
              <Typography
                variant="h6"
                sx={{
                  fontWeight: 400,
                  opacity: 0.8,
                  maxWidth: 400,
                  lineHeight: 1.6,
                }}
              >
                Create professional presentations with McKinsey-style templates
                and best practices built-in.
              </Typography>
            </Box>

            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="body1" sx={{ opacity: 0.7, mb: 1 }}>
                Features:
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                • Professional slide templates
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                • Data visualization tools
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                • Collaboration features
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                • Export to PowerPoint
              </Typography>
            </Box>
          </Grid>

          {/* Right side - Auth forms */}
          <Grid
            item
            xs={12}
            md={6}
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              p: 2,
            }}
          >
            <Paper
              elevation={8}
              sx={{
                p: 4,
                width: '100%',
                maxWidth: 400,
                borderRadius: 3,
                boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
              }}
            >
              <Outlet />
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  )
}

export default AuthLayout