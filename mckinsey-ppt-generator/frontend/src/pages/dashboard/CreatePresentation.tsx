import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { useForm, Controller } from 'react-hook-form'
import {
  Box,
  Typography,
  Container,
  Card,
  CardContent,
  TextField,
  Button,
  Grid,
  Alert,
  CircularProgress,
  Paper,
  Chip,
  Divider,
} from '@mui/material'
import {
  ArrowBack as ArrowBackIcon,
  Create as CreateIcon,
  Slideshow as SlideshowIcon,
  BusinessCenter as BusinessCenterIcon,
  Analytics as AnalyticsIcon,
  School as SchoolIcon,
} from '@mui/icons-material'
import { toast } from 'react-toastify'

import { AppDispatch, RootState } from '../../store/store'
import { createPresentation } from '../../store/presentationSlice'
import { CreatePresentationRequest } from '../../types'

interface CreatePresentationForm extends CreatePresentationRequest {
  template?: string
}

const CreatePresentation: React.FC = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch<AppDispatch>()
  const { isLoading, error } = useSelector((state: RootState) => state.presentation)

  const {
    control,
    handleSubmit,
    watch,
    setValue,
    formState: { errors },
  } = useForm<CreatePresentationForm>({
    defaultValues: {
      title: '',
      description: '',
      template: '',
    },
  })

  const selectedTemplate = watch('template')

  const templates = [
    {
      id: 'executive-summary',
      name: 'Executive Summary',
      description: 'Perfect for C-level presentations and board meetings',
      icon: <BusinessCenterIcon />,
      color: '#0070C0',
      slides: ['Title Slide', 'Executive Summary', 'Key Findings', 'Recommendations', 'Next Steps'],
    },
    {
      id: 'data-analysis',
      name: 'Data Analysis',
      description: 'Ideal for presenting analytical findings and insights',
      icon: <AnalyticsIcon />,
      color: '#00A651',
      slides: ['Title Slide', 'Problem Statement', 'Methodology', 'Key Findings', 'Data Insights', 'Conclusions'],
    },
    {
      id: 'strategy-proposal',
      name: 'Strategy Proposal',
      description: 'Great for strategic initiatives and business proposals',
      icon: <SlideshowIcon />,
      color: '#FF6B35',
      slides: ['Title Slide', 'Current State', 'Problem Definition', 'Proposed Strategy', 'Implementation Plan', 'Expected Outcomes'],
    },
    {
      id: 'training-material',
      name: 'Training Material',
      description: 'Designed for educational and training presentations',
      icon: <SchoolIcon />,
      color: '#8E44AD',
      slides: ['Title Slide', 'Learning Objectives', 'Content Overview', 'Key Concepts', 'Examples', 'Summary & Q&A'],
    },
  ]

  const onSubmit = async (data: CreatePresentationForm) => {
    try {
      const { template, ...presentationData } = data
      const result = await dispatch(createPresentation(presentationData))
      if (createPresentation.fulfilled.match(result)) {
        const presentationId = result.payload.id
        toast.success('Presentation created successfully!')
        navigate(`/presentations/${presentationId}/edit`)
      } else {
        toast.error(result.payload as string || 'Failed to create presentation')
      }
    } catch (error) {
      toast.error('An unexpected error occurred')
    }
  }

  const handleTemplateSelect = (templateId: string) => {
    setValue('template', templateId)
  }

  const handleBack = () => {
    navigate('/presentations')
  }

  const TemplateCard: React.FC<{
    template: typeof templates[0]
    isSelected: boolean
    onSelect: () => void
  }> = ({ template, isSelected, onSelect }) => (
    <Card
      sx={{
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        border: isSelected ? `2px solid ${template.color}` : '2px solid transparent',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: 3,
        },
        ...(isSelected && {
          boxShadow: `0 4px 20px ${template.color}30`,
        }),
      }}
      onClick={onSelect}
    >
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Box sx={{ color: template.color, mr: 2 }}>
            {template.icon}
          </Box>
          <Typography variant="h6" fontWeight="bold">
            {template.name}
          </Typography>
          {isSelected && (
            <Chip
              label="Selected"
              size="small"
              sx={{ ml: 'auto', bgcolor: template.color, color: 'white' }}
            />
          )}
        </Box>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {template.description}
        </Typography>
        <Divider sx={{ my: 2 }} />
        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
          Includes {template.slides.length} slides:
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {template.slides.map((slide, index) => (
            <Chip
              key={index}
              label={slide}
              size="small"
              variant="outlined"
              sx={{ fontSize: '0.7rem' }}
            />
          ))}
        </Box>
      </CardContent>
    </Card>
  )

  return (
    <Container maxWidth="lg">
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleBack}
          sx={{ mb: 2 }}
        >
          Back to Presentations
        </Button>
        <Typography
          variant="h3"
          component="h1"
          gutterBottom
          sx={{ fontWeight: 700, color: 'primary.main' }}
        >
          Create New Presentation
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Choose a template and provide details for your new presentation
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {/* Template Selection */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h5" fontWeight="bold" gutterBottom>
              Choose a Template
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Select a McKinsey-style template that best fits your presentation needs
            </Typography>
            <Grid container spacing={3}>
              {templates.map((template) => (
                <Grid item xs={12} sm={6} key={template.id}>
                  <TemplateCard
                    template={template}
                    isSelected={selectedTemplate === template.id}
                    onSelect={() => handleTemplateSelect(template.id)}
                  />
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Form */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, position: 'sticky', top: 24 }}>
            <Typography variant="h5" fontWeight="bold" gutterBottom>
              Presentation Details
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Provide a title and description for your presentation
            </Typography>

            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
              <Controller
                name="title"
                control={control}
                rules={{
                  required: 'Title is required',
                  minLength: {
                    value: 3,
                    message: 'Title must be at least 3 characters',
                  },
                  maxLength: {
                    value: 100,
                    message: 'Title must be less than 100 characters',
                  },
                }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Presentation Title"
                    placeholder="Enter a descriptive title..."
                    margin="normal"
                    error={!!errors.title}
                    helperText={errors.title?.message}
                    disabled={isLoading}
                    sx={{ mb: 3 }}
                  />
                )}
              />

              <Controller
                name="description"
                control={control}
                rules={{
                  required: 'Description is required',
                  minLength: {
                    value: 10,
                    message: 'Description must be at least 10 characters',
                  },
                  maxLength: {
                    value: 500,
                    message: 'Description must be less than 500 characters',
                  },
                }}
                render={({ field }) => (
                  <TextField
                    {...field}
                    fullWidth
                    label="Description"
                    placeholder="Briefly describe your presentation..."
                    multiline
                    rows={4}
                    margin="normal"
                    error={!!errors.description}
                    helperText={errors.description?.message}
                    disabled={isLoading}
                    sx={{ mb: 3 }}
                  />
                )}
              />

              {selectedTemplate && (
                <Alert severity="info" sx={{ mb: 3 }}>
                  <Typography variant="body2">
                    Template selected: {templates.find(t => t.id === selectedTemplate)?.name}
                  </Typography>
                </Alert>
              )}

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={isLoading || !selectedTemplate}
                startIcon={isLoading ? <CircularProgress size={20} /> : <CreateIcon />}
                sx={{
                  py: 1.5,
                  fontWeight: 600,
                  textTransform: 'none',
                  borderRadius: 2,
                  boxShadow: '0 4px 12px rgba(0, 112, 192, 0.3)',
                  '&:hover': {
                    boxShadow: '0 6px 16px rgba(0, 112, 192, 0.4)',
                  },
                }}
              >
                {isLoading ? 'Creating...' : 'Create Presentation'}
              </Button>

              {!selectedTemplate && (
                <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block', textAlign: 'center' }}>
                  Please select a template to continue
                </Typography>
              )}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  )
}

export default CreatePresentation