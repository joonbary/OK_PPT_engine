import React, { useState } from 'react'
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  IconButton,
  Box,
  Chip,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  Skeleton,
} from '@mui/material'
import {
  MoreVert as MoreVertIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  ContentCopy as ContentCopyIcon,
  Visibility as VisibilityIcon,
  DragIndicator as DragIndicatorIcon,
} from '@mui/icons-material'

import { Slide, SlideLayoutType } from '../types'

interface SlideCardProps {
  slide: Slide
  slideNumber: number
  isSelected?: boolean
  isDragging?: boolean
  onSelect?: () => void
  onEdit?: () => void
  onDelete?: () => void
  onDuplicate?: () => void
  onPreview?: () => void
  loading?: boolean
}

const SlideCard: React.FC<SlideCardProps> = ({
  slide,
  slideNumber,
  isSelected = false,
  isDragging = false,
  onSelect,
  onEdit,
  onDelete,
  onDuplicate,
  onPreview,
  loading = false,
}) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)

  const layoutLabels: Record<SlideLayoutType, string> = {
    title_slide: 'Title Slide',
    content_slide: 'Content',
    two_column: 'Two Column',
    bullet_points: 'Bullet Points',
    chart_slide: 'Chart',
    image_slide: 'Image',
    conclusion_slide: 'Conclusion',
  }

  const layoutColors: Record<SlideLayoutType, string> = {
    title_slide: '#0070C0',
    content_slide: '#00A651',
    two_column: '#FF6B35',
    bullet_points: '#8E44AD',
    chart_slide: '#F39C12',
    image_slide: '#E74C3C',
    conclusion_slide: '#2C3E50',
  }

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>) => {
    event.stopPropagation()
    setAnchorEl(event.currentTarget)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
  }

  const handleMenuAction = (action: () => void) => {
    action()
    handleMenuClose()
  }

  const handleCardClick = () => {
    if (onSelect) {
      onSelect()
    }
  }

  if (loading) {
    return (
      <Card sx={{ height: 180 }}>
        <CardContent sx={{ height: '100%', p: 2 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
            <Skeleton variant="text" width="20%" height={24} />
            <Skeleton variant="circular" width={24} height={24} />
          </Box>
          <Skeleton variant="text" width="80%" height={20} sx={{ mb: 1 }} />
          <Skeleton variant="text" width="60%" height={16} sx={{ mb: 2 }} />
          <Skeleton variant="rectangular" width="40%" height={20} />
        </CardContent>
      </Card>
    )
  }

  const layoutType = slide.layout_type as SlideLayoutType
  const layoutLabel = layoutLabels[layoutType] || layoutType
  const layoutColor = layoutColors[layoutType] || '#666'

  return (
    <Card
      sx={{
        height: 180,
        cursor: 'pointer',
        transition: 'all 0.2s ease-in-out',
        border: isSelected ? `2px solid ${layoutColor}` : '2px solid transparent',
        opacity: isDragging ? 0.5 : 1,
        transform: isSelected ? 'scale(1.02)' : 'scale(1)',
        '&:hover': {
          transform: isSelected ? 'scale(1.02)' : 'scale(1.01)',
          boxShadow: 3,
        },
        ...(isSelected && {
          boxShadow: `0 4px 20px ${layoutColor}30`,
        }),
      }}
      onClick={handleCardClick}
    >
      <CardContent sx={{ height: '100%', p: 2, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <DragIndicatorIcon
              sx={{
                color: 'action.active',
                mr: 1,
                fontSize: 16,
                opacity: 0.6,
              }}
            />
            <Typography
              variant="subtitle2"
              sx={{
                color: layoutColor,
                fontWeight: 'bold',
                fontSize: '0.8rem',
              }}
            >
              Slide {slideNumber}
            </Typography>
          </Box>
          <IconButton
            size="small"
            onClick={handleMenuClick}
            sx={{
              opacity: 0.7,
              '&:hover': { opacity: 1 },
            }}
          >
            <MoreVertIcon fontSize="small" />
          </IconButton>
        </Box>

        {/* Content */}
        <Box sx={{ flexGrow: 1, mb: 2 }}>
          <Typography
            variant="subtitle1"
            sx={{
              fontWeight: 600,
              mb: 1,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              display: '-webkit-box',
              WebkitLineClamp: 2,
              WebkitBoxOrient: 'vertical',
              lineHeight: 1.3,
              fontSize: '0.9rem',
            }}
          >
            {slide.title || 'Untitled Slide'}
          </Typography>
          <Typography
            variant="body2"
            color="text.secondary"
            sx={{
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              display: '-webkit-box',
              WebkitLineClamp: 2,
              WebkitBoxOrient: 'vertical',
              lineHeight: 1.4,
              fontSize: '0.8rem',
            }}
          >
            {slide.content || 'No content'}
          </Typography>
        </Box>

        {/* Footer */}
        <Box sx={{ mt: 'auto' }}>
          <Chip
            label={layoutLabel}
            size="small"
            sx={{
              backgroundColor: `${layoutColor}15`,
              color: layoutColor,
              fontWeight: 'bold',
              fontSize: '0.7rem',
              height: 22,
              '& .MuiChip-label': {
                px: 1,
              },
            }}
          />
        </Box>
      </CardContent>

      {/* Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        PaperProps={{
          sx: { minWidth: 160 },
        }}
      >
        {onPreview && (
          <MenuItem onClick={() => handleMenuAction(onPreview)}>
            <ListItemIcon>
              <VisibilityIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Preview" />
          </MenuItem>
        )}
        {onEdit && (
          <MenuItem onClick={() => handleMenuAction(onEdit)}>
            <ListItemIcon>
              <EditIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Edit" />
          </MenuItem>
        )}
        {onDuplicate && (
          <MenuItem onClick={() => handleMenuAction(onDuplicate)}>
            <ListItemIcon>
              <ContentCopyIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Duplicate" />
          </MenuItem>
        )}
        {onDelete && (
          <MenuItem 
            onClick={() => handleMenuAction(onDelete)}
            sx={{ color: 'error.main' }}
          >
            <ListItemIcon>
              <DeleteIcon fontSize="small" sx={{ color: 'error.main' }} />
            </ListItemIcon>
            <ListItemText primary="Delete" />
          </MenuItem>
        )}
      </Menu>
    </Card>
  )
}

export default SlideCard