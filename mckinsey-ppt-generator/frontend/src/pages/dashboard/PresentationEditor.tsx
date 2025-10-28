import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import {
  Box,
  Typography,
  Container,
  Paper,
  Grid,
  Button,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  ListItemIcon,
  TextField,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Fab,
  Skeleton,
  Alert,
  Divider,
  Chip,
  Menu,
  MenuItem,
} from '@mui/material'
import {
  ArrowBack as ArrowBackIcon,
  Add as AddIcon,
  Save as SaveIcon,
  Preview as PreviewIcon,
  Download as DownloadIcon,
  Settings as SettingsIcon,
  Slideshow as SlideshowIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  DragIndicator as DragIndicatorIcon,
  MoreVert as MoreVertIcon,
} from '@mui/icons-material'
import { toast } from 'react-toastify'

import { AppDispatch, RootState } from '../../store/store'
import { fetchPresentation, updatePresentation } from '../../store/presentationSlice'
import { Slide, SlideLayoutType } from '../../types'
import LoadingSpinner from '../../components/LoadingSpinner'

const PresentationEditor: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const dispatch = useDispatch<AppDispatch>()
  const { currentPresentation, isLoading, error } = useSelector((state: RootState) => state.presentation)

  const [selectedSlideIndex, setSelectedSlideIndex] = useState(0)
  const [isAddSlideDialogOpen, setIsAddSlideDialogOpen] = useState(false)
  const [slideTitle, setSlideTitle] = useState('')
  const [slideContent, setSlideContent] = useState('')
  const [slideLayout, setSlideLayout] = useState<SlideLayoutType>('content_slide')
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [selectedSlide, setSelectedSlide] = useState<Slide | null>(null)

  useEffect(() => {
    if (id) {
      dispatch(fetchPresentation(id))
    }
  }, [dispatch, id])

  useEffect(() => {
    if (currentPresentation?.slides && selectedSlideIndex < currentPresentation.slides.length) {
      const slide = currentPresentation.slides[selectedSlideIndex]
      setSlideTitle(slide.title)
      setSlideContent(slide.content)
      setSlideLayout(slide.layout_type as SlideLayoutType)
    }
  }, [currentPresentation, selectedSlideIndex])

  const slideLayouts: { value: SlideLayoutType; label: string; description: string }[] = [
    { value: 'title_slide', label: 'Title Slide', description: 'Main title and subtitle' },
    { value: 'content_slide', label: 'Content Slide', description: 'General content layout' },
    { value: 'two_column', label: 'Two Column', description: 'Side-by-side content' },
    { value: 'bullet_points', label: 'Bullet Points', description: 'List of key points' },
    { value: 'chart_slide', label: 'Chart Slide', description: 'Data visualization' },
    { value: 'image_slide', label: 'Image Slide', description: 'Image with caption' },
    { value: 'conclusion_slide', label: 'Conclusion', description: 'Summary and next steps' },
  ]

  const handleBack = () => {
    navigate('/presentations')
  }

  const handleSavePresentation = async () => {
    if (!currentPresentation) return

    try {
      await dispatch(updatePresentation({
        id: currentPresentation.id,
        data: {
          title: currentPresentation.title,
          description: currentPresentation.description,
        },
      }))
      toast.success('Presentation saved successfully!')
    } catch (error) {
      toast.error('Failed to save presentation')
    }
  }

  const handleSlideSelect = (index: number) => {
    setSelectedSlideIndex(index)
  }

  const handleAddSlide = () => {
    setIsAddSlideDialogOpen(true)
    setSlideTitle('')
    setSlideContent('')
    setSlideLayout('content_slide')
  }

  const handleAddSlideConfirm = () => {
    // TODO: Implement add slide logic
    toast.info('Add slide feature coming soon')
    setIsAddSlideDialogOpen(false)
  }

  const handleSlideMenuClick = (event: React.MouseEvent<HTMLElement>, slide: Slide) => {
    setAnchorEl(event.currentTarget)
    setSelectedSlide(slide)
  }

  const handleSlideMenuClose = () => {
    setAnchorEl(null)
    setSelectedSlide(null)
  }

  const handleDeleteSlide = () => {
    // TODO: Implement delete slide logic
    toast.info('Delete slide feature coming soon')
    handleSlideMenuClose()
  }

  const handleDuplicateSlide = () => {
    // TODO: Implement duplicate slide logic
    toast.info('Duplicate slide feature coming soon')
    handleSlideMenuClose()
  }

  const handlePreview = () => {
    toast.info('Preview feature coming soon')
  }

  const handleExport = () => {
    toast.info('Export feature coming soon')
  }

  if (isLoading) {
    return <LoadingSpinner />
  }

  if (error) {
    return (
      <Container maxWidth="lg">
        <Alert severity="error" sx={{ mt: 3 }}>
          {error}
        </Alert>
      </Container>
    )
  }

  if (!currentPresentation) {
    return (
      <Container maxWidth="lg">
        <Alert severity="warning" sx={{ mt: 3 }}>
          Presentation not found
        </Alert>
      </Container>
    )
  }

  const currentSlide = currentPresentation.slides[selectedSlideIndex]

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Paper
        elevation={1}
        sx={{
          px: 3,
          py: 2,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderRadius: 0,
        }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={handleBack}
            sx={{ mr: 3 }}
          >
            Back
          </Button>
          <Typography variant="h6" fontWeight="bold">
            {currentPresentation.title}
          </Typography>
          <Chip
            label={`${currentPresentation.slides.length} slides`}
            size="small"
            variant="outlined"
            sx={{ ml: 2 }}
          />
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Button
            variant="outlined"
            startIcon={<PreviewIcon />}
            onClick={handlePreview}
          >
            Preview
          </Button>
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={handleExport}
          >
            Export
          </Button>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSavePresentation}
          >
            Save
          </Button>
        </Box>
      </Paper>

      {/* Main Content */}
      <Box sx={{ flexGrow: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Slide Thumbnails */}
        <Paper
          sx={{
            width: 280,
            borderRadius: 0,
            borderRight: 1,
            borderColor: 'divider',
            overflow: 'auto',
          }}
        >
          <Box sx={{ p: 2 }}>
            <Button
              fullWidth
              variant="outlined"
              startIcon={<AddIcon />}
              onClick={handleAddSlide}
              sx={{ mb: 2 }}
            >
              Add Slide
            </Button>
          </Box>
          <List dense>
            {currentPresentation.slides.map((slide, index) => (
              <ListItem key={slide.id} disablePadding>
                <ListItemButton
                  selected={selectedSlideIndex === index}
                  onClick={() => handleSlideSelect(index)}
                  sx={{
                    py: 1.5,
                    px: 2,
                    '&.Mui-selected': {
                      backgroundColor: 'primary.main',
                      color: 'primary.contrastText',
                      '&:hover': {
                        backgroundColor: 'primary.dark',
                      },
                    },
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 36 }}>
                    <DragIndicatorIcon
                      sx={{
                        color: selectedSlideIndex === index ? 'inherit' : 'action.active',
                      }}
                    />
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Typography
                        variant="body2"
                        sx={{
                          fontWeight: selectedSlideIndex === index ? 'bold' : 'normal',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {index + 1}. {slide.title || 'Untitled Slide'}
                      </Typography>
                    }
                    secondary={
                      <Typography
                        variant="caption"
                        sx={{
                          color: selectedSlideIndex === index ? 'inherit' : 'text.secondary',
                          opacity: selectedSlideIndex === index ? 0.8 : 1,
                        }}
                      >
                        {slideLayouts.find(l => l.value === slide.layout_type)?.label || slide.layout_type}
                      </Typography>
                    }
                  />
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleSlideMenuClick(e, slide)
                    }}
                    sx={{
                      color: selectedSlideIndex === index ? 'inherit' : 'action.active',
                    }}
                  >
                    <MoreVertIcon fontSize="small" />
                  </IconButton>
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Paper>

        {/* Main Editor */}
        <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
          {/* Slide Canvas */}
          <Box
            sx={{
              flexGrow: 1,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: 'grey.100',
              p: 3,
            }}
          >
            <Paper
              sx={{
                width: '100%',
                maxWidth: 800,
                aspectRatio: '16/9',
                p: 4,
                display: 'flex',
                flexDirection: 'column',
                boxShadow: 3,
              }}
            >
              {currentSlide ? (
                <>
                  <Typography
                    variant="h4"
                    component="h1"
                    gutterBottom
                    sx={{
                      fontWeight: 'bold',
                      color: 'primary.main',
                      textAlign: slideLayout === 'title_slide' ? 'center' : 'left',
                    }}
                  >
                    {currentSlide.title || 'Slide Title'}
                  </Typography>
                  <Divider sx={{ mb: 3 }} />
                  <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
                    <Typography
                      variant="body1"
                      sx={{
                        whiteSpace: 'pre-wrap',
                        lineHeight: 1.6,
                        textAlign: slideLayout === 'title_slide' ? 'center' : 'left',
                      }}
                    >
                      {currentSlide.content || 'Slide content goes here...'}
                    </Typography>
                  </Box>
                </>
              ) : (
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                  <Typography variant="h6" color="text.secondary">
                    Select a slide to edit
                  </Typography>
                </Box>
              )}
            </Paper>
          </Box>

          {/* Properties Panel */}
          <Paper
            sx={{
              height: 250,
              borderRadius: 0,
              borderTop: 1,
              borderColor: 'divider',
              p: 3,
              overflow: 'auto',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Slide Properties
            </Typography>
            {currentSlide && (
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <TextField
                    fullWidth
                    label="Slide Title"
                    value={slideTitle}
                    onChange={(e) => setSlideTitle(e.target.value)}
                    size="small"
                  />
                </Grid>
                <Grid item xs={12} md={4}>
                  <TextField
                    select
                    fullWidth
                    label="Layout"
                    value={slideLayout}
                    onChange={(e) => setSlideLayout(e.target.value as SlideLayoutType)}
                    size="small"
                  >
                    {slideLayouts.map((layout) => (
                      <MenuItem key={layout.value} value={layout.value}>
                        {layout.label}
                      </MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Button
                    variant="outlined"
                    startIcon={<SettingsIcon />}
                    size="small"
                  >
                    Advanced Settings
                  </Button>
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Slide Content"
                    value={slideContent}
                    onChange={(e) => setSlideContent(e.target.value)}
                    multiline
                    rows={3}
                    placeholder="Enter slide content..."
                  />
                </Grid>
              </Grid>
            )}
          </Paper>
        </Box>
      </Box>

      {/* Add Slide Dialog */}
      <Dialog
        open={isAddSlideDialogOpen}
        onClose={() => setIsAddSlideDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Add New Slide</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Slide Title"
            value={slideTitle}
            onChange={(e) => setSlideTitle(e.target.value)}
            margin="normal"
          />
          <TextField
            select
            fullWidth
            label="Layout"
            value={slideLayout}
            onChange={(e) => setSlideLayout(e.target.value as SlideLayoutType)}
            margin="normal"
          >
            {slideLayouts.map((layout) => (
              <MenuItem key={layout.value} value={layout.value}>
                <Box>
                  <Typography variant="body1">{layout.label}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {layout.description}
                  </Typography>
                </Box>
              </MenuItem>
            ))}
          </TextField>
          <TextField
            fullWidth
            label="Content"
            value={slideContent}
            onChange={(e) => setSlideContent(e.target.value)}
            multiline
            rows={4}
            margin="normal"
            placeholder="Enter slide content..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsAddSlideDialogOpen(false)}>
            Cancel
          </Button>
          <Button onClick={handleAddSlideConfirm} variant="contained">
            Add Slide
          </Button>
        </DialogActions>
      </Dialog>

      {/* Slide Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleSlideMenuClose}
      >
        <MenuItem onClick={handleDuplicateSlide}>
          <EditIcon fontSize="small" sx={{ mr: 1 }} />
          Duplicate
        </MenuItem>
        <MenuItem onClick={handleDeleteSlide} sx={{ color: 'error.main' }}>
          <DeleteIcon fontSize="small" sx={{ mr: 1 }} />
          Delete
        </MenuItem>
      </Menu>
    </Box>
  )
}

export default PresentationEditor