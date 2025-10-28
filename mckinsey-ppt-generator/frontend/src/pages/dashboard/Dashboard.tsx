import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Container,
  Chip,
  IconButton,
  Skeleton,
} from '@mui/material'
import {
  Add as AddIcon,
  Slideshow as SlideshowIcon,
  Edit as EditIcon,
  Share as ShareIcon,
  Download as DownloadIcon,
  Analytics as AnalyticsIcon,
} from '@mui/icons-material'

import { AppDispatch, RootState } from '../../store/store'
import { fetchPresentations } from '../../store/presentationSlice'
import { Presentation } from '../../types'

const Dashboard: React.FC = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch<AppDispatch>()
  const { user } = useSelector((state: RootState) => state.auth)
  const { presentations, isLoading } = useSelector((state: RootState) => state.presentation)

  useEffect(() => {
    dispatch(fetchPresentations())
  }, [dispatch])

  const recentPresentations = presentations.slice(0, 6)

  const handleCreateNew = () => {
    navigate('/presentations/new')
  }

  const handleViewAll = () => {
    navigate('/presentations')
  }

  const handleEditPresentation = (id: string) => {
    navigate(`/presentations/${id}/edit`)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  const StatCard: React.FC<{
    title: string
    value: string | number
    icon: React.ReactNode
    color: string
  }> = ({ title, value, icon, color }) => (
    <Card
      sx={{
        height: '100%',
        background: `linear-gradient(135deg, ${color}15 0%, ${color}05 100%)`,
        border: `1px solid ${color}20`,
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box sx={{ color, mr: 2 }}>{icon}</Box>
          <Typography variant="h6" color="text.secondary">
            {title}
          </Typography>
        </Box>
        <Typography variant="h3" fontWeight="bold" color={color}>
          {value}
        </Typography>
      </CardContent>
    </Card>
  )

  const PresentationCard: React.FC<{ presentation: Presentation }> = ({
    presentation,
  }) => (
    <Card
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: 3,
        },
      }}
    >
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 2 }}>
          <SlideshowIcon
            sx={{ color: 'primary.main', mr: 1.5, mt: 0.5, fontSize: 20 }}
          />
          <Box sx={{ flexGrow: 1 }}>
            <Typography
              variant="h6"
              component="h3"
              gutterBottom
              sx={{
                fontWeight: 600,
                lineHeight: 1.3,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
              }}
            >
              {presentation.title}
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{
                mb: 2,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                display: '-webkit-box',
                WebkitLineClamp: 2,
                WebkitBoxOrient: 'vertical',
              }}
            >
              {presentation.description}
            </Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Chip
            label={`${presentation.slides.length} slides`}
            size="small"
            variant="outlined"
            sx={{ mr: 1 }}
          />
          <Typography variant="caption" color="text.secondary">
            Modified {formatDate(presentation.updated_at)}
          </Typography>
        </Box>
      </CardContent>
      <CardActions sx={{ px: 2, pb: 2 }}>
        <Button
          size="small"
          variant="contained"
          startIcon={<EditIcon />}
          onClick={() => handleEditPresentation(presentation.id)}
          sx={{ mr: 1 }}
        >
          Edit
        </Button>
        <IconButton size="small" color="primary">
          <ShareIcon fontSize="small" />
        </IconButton>
        <IconButton size="small" color="primary">
          <DownloadIcon fontSize="small" />
        </IconButton>
      </CardActions>
    </Card>
  )

  const SkeletonCard: React.FC = () => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Skeleton variant="text" width="80%" height={32} />
        <Skeleton variant="text" width="60%" height={20} sx={{ mt: 1 }} />
        <Skeleton variant="text" width="40%" height={16} sx={{ mt: 2 }} />
      </CardContent>
      <CardActions>
        <Skeleton variant="rectangular" width={80} height={32} sx={{ mr: 1 }} />
        <Skeleton variant="circular" width={32} height={32} sx={{ mr: 1 }} />
        <Skeleton variant="circular" width={32} height={32} />
      </CardActions>
    </Card>
  )

  return (
    <Container maxWidth="xl">
      {/* Welcome Section */}
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{ fontWeight: 700, color: 'primary.main' }}
        >
          Welcome back, {user?.full_name?.split(' ')[0] || 'User'}!
        </Typography>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          Create professional presentations with McKinsey-style templates
        </Typography>
      </Box>

      {/* Stats Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Presentations"
            value={presentations.length}
            icon={<SlideshowIcon />}
            color="#0070C0"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Slides"
            value={presentations.reduce((acc, p) => acc + p.slides.length, 0)}
            icon={<AnalyticsIcon />}
            color="#00A651"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Recent Activity"
            value={
              presentations.filter(
                (p) =>
                  new Date(p.updated_at) >
                  new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
              ).length
            }
            icon={<EditIcon />}
            color="#FF6B35"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              height: '100%',
              background: 'linear-gradient(135deg, #0070C015 0%, #0070C005 100%)',
              border: '1px solid #0070C020',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              '&:hover': {
                transform: 'translateY(-2px)',
                boxShadow: 3,
              },
            }}
            onClick={handleCreateNew}
          >
            <CardContent
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
                textAlign: 'center',
              }}
            >
              <AddIcon sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
              <Typography variant="h6" color="primary.main" fontWeight="bold">
                Create New
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Start a new presentation
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Presentations Section */}
      <Box sx={{ mb: 4 }}>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            mb: 3,
          }}
        >
          <Typography variant="h4" component="h2" fontWeight="bold">
            Recent Presentations
          </Typography>
          {presentations.length > 6 && (
            <Button variant="outlined" onClick={handleViewAll}>
              View All
            </Button>
          )}
        </Box>

        <Grid container spacing={3}>
          {isLoading
            ? Array.from({ length: 6 }).map((_, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <SkeletonCard />
                </Grid>
              ))
            : recentPresentations.length > 0
            ? recentPresentations.map((presentation) => (
                <Grid item xs={12} sm={6} md={4} key={presentation.id}>
                  <PresentationCard presentation={presentation} />
                </Grid>
              ))
            : (
                <Grid item xs={12}>
                  <Card
                    sx={{
                      textAlign: 'center',
                      py: 6,
                      backgroundColor: 'grey.50',
                    }}
                  >
                    <CardContent>
                      <SlideshowIcon
                        sx={{ fontSize: 64, color: 'grey.400', mb: 2 }}
                      />
                      <Typography variant="h6" color="text.secondary" gutterBottom>
                        No presentations yet
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                        Create your first presentation to get started
                      </Typography>
                      <Button
                        variant="contained"
                        startIcon={<AddIcon />}
                        onClick={handleCreateNew}
                      >
                        Create Your First Presentation
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              )}
        </Grid>
      </Box>
    </Container>
  )
}

export default Dashboard