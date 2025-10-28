import React, { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Box,
  Divider,
  ListItemIcon,
  ListItemText,
  Chip,
} from '@mui/material'
import {
  AccountCircle,
  Dashboard as DashboardIcon,
  Slideshow as SlideshowIcon,
  Add as AddIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon,
  Help as HelpIcon,
  Notifications as NotificationsIcon,
} from '@mui/icons-material'
import { toast } from 'react-toastify'

import { AppDispatch, RootState } from '../store/store'
import { logout } from '../store/authSlice'

const Navbar: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const dispatch = useDispatch<AppDispatch>()
  const { user } = useSelector((state: RootState) => state.auth)

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)

  const navigationItems = [
    {
      label: 'Dashboard',
      path: '/dashboard',
      icon: <DashboardIcon />,
    },
    {
      label: 'Presentations',
      path: '/presentations',
      icon: <SlideshowIcon />,
    },
  ]

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleProfileMenuClose = () => {
    setAnchorEl(null)
  }

  const handleNavigation = (path: string) => {
    navigate(path)
  }

  const handleCreateNew = () => {
    navigate('/presentations/new')
  }

  const handleLogout = () => {
    dispatch(logout())
    toast.success('Logged out successfully')
    navigate('/auth/login')
    handleProfileMenuClose()
  }

  const handleSettings = () => {
    toast.info('Settings page coming soon')
    handleProfileMenuClose()
  }

  const handleHelp = () => {
    toast.info('Help center coming soon')
    handleProfileMenuClose()
  }

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((word) => word.charAt(0).toUpperCase())
      .join('')
      .slice(0, 2)
  }

  const isActiveRoute = (path: string) => {
    return location.pathname === path || 
           (path === '/dashboard' && location.pathname === '/') ||
           (path === '/presentations' && location.pathname.startsWith('/presentations'))
  }

  return (
    <AppBar
      position="sticky"
      elevation={1}
      sx={{
        backgroundColor: 'white',
        color: 'text.primary',
        borderBottom: 1,
        borderColor: 'divider',
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        {/* Logo and Brand */}
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box
            sx={{
              width: 40,
              height: 40,
              backgroundColor: 'primary.main',
              borderRadius: 1,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2,
              cursor: 'pointer',
            }}
            onClick={() => handleNavigation('/dashboard')}
          >
            <Typography
              variant="h6"
              sx={{
                color: 'white',
                fontWeight: 'bold',
                fontSize: '1.2rem',
              }}
            >
              M
            </Typography>
          </Box>
          <Typography
            variant="h6"
            component="div"
            sx={{
              fontWeight: 'bold',
              color: 'primary.main',
              cursor: 'pointer',
            }}
            onClick={() => handleNavigation('/dashboard')}
          >
            McKinsey PPT Generator
          </Typography>
        </Box>

        {/* Navigation Links */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {navigationItems.map((item) => (
            <Button
              key={item.path}
              startIcon={item.icon}
              onClick={() => handleNavigation(item.path)}
              sx={{
                color: isActiveRoute(item.path) ? 'primary.main' : 'text.secondary',
                fontWeight: isActiveRoute(item.path) ? 'bold' : 'normal',
                backgroundColor: isActiveRoute(item.path) ? 'primary.50' : 'transparent',
                '&:hover': {
                  backgroundColor: 'primary.50',
                  color: 'primary.main',
                },
                borderRadius: 2,
                px: 2,
                py: 1,
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>

        {/* Action Buttons and Profile */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {/* Create New Button */}
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleCreateNew}
            sx={{
              borderRadius: 2,
              textTransform: 'none',
              fontWeight: 'bold',
              boxShadow: '0 2px 8px rgba(0, 112, 192, 0.3)',
              '&:hover': {
                boxShadow: '0 4px 12px rgba(0, 112, 192, 0.4)',
              },
            }}
          >
            Create New
          </Button>

          {/* Notifications */}
          <IconButton
            size="large"
            color="inherit"
            sx={{ color: 'text.secondary' }}
          >
            <NotificationsIcon />
          </IconButton>

          {/* Profile Menu */}
          <Box sx={{ display: 'flex', alignItems: 'center', ml: 1 }}>
            <IconButton
              size="large"
              edge="end"
              aria-label="account of current user"
              aria-controls="primary-search-account-menu"
              aria-haspopup="true"
              onClick={handleProfileMenuOpen}
              color="inherit"
            >
              <Avatar
                sx={{
                  width: 36,
                  height: 36,
                  backgroundColor: 'primary.main',
                  fontSize: '0.9rem',
                  fontWeight: 'bold',
                }}
              >
                {user ? getInitials(user.full_name) : <AccountCircle />}
              </Avatar>
            </IconButton>
          </Box>
        </Box>

        {/* Profile Dropdown Menu */}
        <Menu
          anchorEl={anchorEl}
          id="primary-search-account-menu"
          keepMounted
          open={Boolean(anchorEl)}
          onClose={handleProfileMenuClose}
          PaperProps={{
            sx: {
              mt: 1,
              minWidth: 280,
              boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
              border: 1,
              borderColor: 'divider',
            },
          }}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        >
          {/* User Info */}
          <Box sx={{ px: 3, py: 2 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Avatar
                sx={{
                  width: 48,
                  height: 48,
                  backgroundColor: 'primary.main',
                  fontSize: '1.1rem',
                  fontWeight: 'bold',
                  mr: 2,
                }}
              >
                {user ? getInitials(user.full_name) : <AccountCircle />}
              </Avatar>
              <Box>
                <Typography variant="subtitle1" fontWeight="bold">
                  {user?.full_name || 'User'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {user?.email || 'user@example.com'}
                </Typography>
              </Box>
            </Box>
            <Chip
              label="Pro User"
              size="small"
              color="primary"
              sx={{ fontWeight: 'bold' }}
            />
          </Box>

          <Divider />

          {/* Menu Items */}
          <MenuItem onClick={handleSettings}>
            <ListItemIcon>
              <SettingsIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Settings" />
          </MenuItem>

          <MenuItem onClick={handleHelp}>
            <ListItemIcon>
              <HelpIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Help & Support" />
          </MenuItem>

          <Divider />

          <MenuItem onClick={handleLogout} sx={{ color: 'error.main' }}>
            <ListItemIcon>
              <LogoutIcon fontSize="small" sx={{ color: 'error.main' }} />
            </ListItemIcon>
            <ListItemText primary="Sign Out" />
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  )
}

export default Navbar