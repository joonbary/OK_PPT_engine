import React, { useEffect, useState } from 'react'
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
  TextField,
  InputAdornment,
  Chip,
  IconButton,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Fab,
  Skeleton,
  Alert,
} from '@mui/material'
import {
  Search as SearchIcon,
  Add as AddIcon,
  Slideshow as SlideshowIcon,
  Edit as EditIcon,
  Share as ShareIcon,
  Download as DownloadIcon,
  MoreVert as MoreVertIcon,
  Delete as DeleteIcon,
  ContentCopy as ContentCopyIcon,
  Sort as SortIcon,
} from '@mui/icons-material'
import { toast } from 'react-toastify'

import { AppDispatch, RootState } from '../../store/store'
import { fetchPresentations, deletePresentation } from '../../store/presentationSlice'
import { Presentation } from '../../types'

const PresentationList: React.FC = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch<AppDispatch>()
  const { presentations, isLoading, error } = useSelector((state: RootState) => state.presentation)

  const [searchTerm, setSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState<'updated' | 'created' | 'title'>('updated')
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [selectedPresentation, setSelectedPresentation] = useState<Presentation | null>(null)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)

  useEffect(() => {
    dispatch(fetchPresentations())
  }, [dispatch])

  const filteredAndSortedPresentations = presentations
    .filter((presentation) =>
      presentation.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      presentation.description.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      switch (sortBy) {
        case 'title':
          return a.title.localeCompare(b.title)
        case 'created':
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        case 'updated':
        default:
          return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
      }
    })

  const handleCreateNew = () => {
    navigate('/presentations/new')
  }

  const handleEditPresentation = (id: string) => {
    navigate(`/presentations/${id}/edit`)
  }

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, presentation: Presentation) => {
    setAnchorEl(event.currentTarget)
    setSelectedPresentation(presentation)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
    setSelectedPresentation(null)
  }

  const handleDeleteClick = () => {
    setDeleteDialogOpen(true)
    handleMenuClose()
  }

  const handleDeleteConfirm = async () => {
    if (selectedPresentation) {
      try {
        await dispatch(deletePresentation(selectedPresentation.id))
        toast.success('Presentation deleted successfully')
        setDeleteDialogOpen(false)
        setSelectedPresentation(null)
      } catch (error) {
        toast.error('Failed to delete presentation')
      }
    }
  }

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false)
    setSelectedPresentation(null)
  }

  const handleDuplicatePresentation = () => {
    // TODO: Implement duplication logic
    toast.info('Duplication feature coming soon')
    handleMenuClose()
  }

  const handleSharePresentation = () => {
    // TODO: Implement sharing logic
    toast.info('Sharing feature coming soon')
    handleMenuClose()
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

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
            sx={{ color: 'primary.main', mr: 1.5, mt: 0.5, fontSize: 24 }}
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
                WebkitLineClamp: 3,
                WebkitBoxOrient: 'vertical',
              }}
            >
              {presentation.description}
            </Typography>
          </Box>
          <IconButton
            size="small"
            onClick={(e) => handleMenuClick(e, presentation)}
          >
            <MoreVertIcon />
          </IconButton>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 1, mb: 2 }}>
          <Chip
            label={`${presentation.slides.length} slides`}
            size="small"
            variant="outlined"
            color="primary"
          />
          <Typography variant="caption" color="text.secondary">
            Updated {formatDate(presentation.updated_at)}
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
        <IconButton size="small" color="primary" onClick={handleSharePresentation}>
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
        <Box sx={{ display: 'flex', mb: 2 }}>
          <Skeleton variant="circular" width={24} height={24} sx={{ mr: 1.5, mt: 0.5 }} />
          <Box sx={{ flexGrow: 1 }}>
            <Skeleton variant="text" width="80%" height={32} />
            <Skeleton variant="text" width="60%" height={20} sx={{ mt: 1 }} />
            <Skeleton variant="text" width="40%" height={16} sx={{ mt: 2 }} />
          </Box>
        </Box>
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
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{ fontWeight: 700, color: 'primary.main' }}
        >
          All Presentations
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Manage and organize your McKinsey-style presentations
        </Typography>
      </Box>

      {/* Search and Filters */}
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={8}>
            <TextField
              fullWidth
              placeholder="Search presentations..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="action" />
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                },
              }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              select
              fullWidth
              label="Sort by"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as 'updated' | 'created' | 'title')}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SortIcon color="action" />
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                },
              }}
            >
              <MenuItem value="updated">Last Updated</MenuItem>
              <MenuItem value="created">Date Created</MenuItem>
              <MenuItem value="title">Title (A-Z)</MenuItem>
            </TextField>
          </Grid>
        </Grid>
      </Box>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Results Summary */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="body1" color="text.secondary">
          {isLoading
            ? 'Loading presentations...'
            : `Showing ${filteredAndSortedPresentations.length} of ${presentations.length} presentations`}
        </Typography>
      </Box>

      {/* Presentations Grid */}
      <Grid container spacing={3}>
        {isLoading
          ? Array.from({ length: 6 }).map((_, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <SkeletonCard />
              </Grid>
            ))
          : filteredAndSortedPresentations.length > 0
          ? filteredAndSortedPresentations.map((presentation) => (
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
                      {searchTerm
                        ? 'No presentations found'
                        : 'No presentations yet'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                      {searchTerm
                        ? 'Try adjusting your search criteria'
                        : 'Create your first presentation to get started'}
                    </Typography>
                    <Button
                      variant="contained"
                      startIcon={<AddIcon />}
                      onClick={handleCreateNew}
                    >
                      Create New Presentation
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            )}
      </Grid>

      {/* Floating Action Button */}
      <Fab
        color="primary"
        aria-label="add"
        sx={{
          position: 'fixed',
          bottom: 24,
          right: 24,
          boxShadow: 3,
        }}
        onClick={handleCreateNew}
      >
        <AddIcon />
      </Fab>

      {/* Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        PaperProps={{
          sx: { minWidth: 180 },
        }}
      >
        <MenuItem onClick={() => selectedPresentation && handleEditPresentation(selectedPresentation.id)}>
          <EditIcon fontSize="small" sx={{ mr: 1 }} />
          Edit
        </MenuItem>
        <MenuItem onClick={handleDuplicatePresentation}>
          <ContentCopyIcon fontSize="small" sx={{ mr: 1 }} />
          Duplicate
        </MenuItem>
        <MenuItem onClick={handleSharePresentation}>
          <ShareIcon fontSize="small" sx={{ mr: 1 }} />
          Share
        </MenuItem>
        <MenuItem onClick={handleDeleteClick} sx={{ color: 'error.main' }}>
          <DeleteIcon fontSize="small" sx={{ mr: 1 }} />
          Delete
        </MenuItem>
      </Menu>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={handleDeleteCancel}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Delete Presentation</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete "{selectedPresentation?.title}"?
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteCancel}>Cancel</Button>
          <Button
            onClick={handleDeleteConfirm}
            color="error"
            variant="contained"
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  )
}

export default PresentationList