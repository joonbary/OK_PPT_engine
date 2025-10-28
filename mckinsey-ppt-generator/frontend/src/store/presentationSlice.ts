import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import {
  PresentationState,
  Presentation,
  Slide,
  CreatePresentationRequest,
  UpdatePresentationRequest,
  CreateSlideRequest,
  UpdateSlideRequest,
} from '../types'
import { presentationService } from '../services/presentation.service'

// Initial state
const initialState: PresentationState = {
  presentations: [],
  currentPresentation: null,
  isLoading: false,
  error: null,
}

// Async thunks for presentations
export const fetchPresentations = createAsyncThunk<
  Presentation[],
  void,
  { rejectValue: string }
>(
  'presentation/fetchPresentations',
  async (_, { rejectWithValue }) => {
    try {
      const response = await presentationService.getPresentations()
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to fetch presentations'
      return rejectWithValue(message)
    }
  }
)

export const fetchPresentation = createAsyncThunk<
  Presentation,
  string,
  { rejectValue: string }
>(
  'presentation/fetchPresentation',
  async (id, { rejectWithValue }) => {
    try {
      const response = await presentationService.getPresentation(id)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to fetch presentation'
      return rejectWithValue(message)
    }
  }
)

export const createPresentation = createAsyncThunk<
  Presentation,
  CreatePresentationRequest,
  { rejectValue: string }
>(
  'presentation/createPresentation',
  async (data, { rejectWithValue }) => {
    try {
      const response = await presentationService.createPresentation(data)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to create presentation'
      return rejectWithValue(message)
    }
  }
)

export const updatePresentation = createAsyncThunk<
  Presentation,
  { id: string; data: UpdatePresentationRequest },
  { rejectValue: string }
>(
  'presentation/updatePresentation',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await presentationService.updatePresentation(id, data)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to update presentation'
      return rejectWithValue(message)
    }
  }
)

export const deletePresentation = createAsyncThunk<
  string,
  string,
  { rejectValue: string }
>(
  'presentation/deletePresentation',
  async (id, { rejectWithValue }) => {
    try {
      await presentationService.deletePresentation(id)
      return id
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to delete presentation'
      return rejectWithValue(message)
    }
  }
)

export const duplicatePresentation = createAsyncThunk<
  Presentation,
  string,
  { rejectValue: string }
>(
  'presentation/duplicatePresentation',
  async (id, { rejectWithValue }) => {
    try {
      const response = await presentationService.duplicatePresentation(id)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to duplicate presentation'
      return rejectWithValue(message)
    }
  }
)

// Async thunks for slides
export const fetchSlides = createAsyncThunk<
  Slide[],
  string,
  { rejectValue: string }
>(
  'presentation/fetchSlides',
  async (presentationId, { rejectWithValue }) => {
    try {
      const response = await presentationService.getSlides(presentationId)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to fetch slides'
      return rejectWithValue(message)
    }
  }
)

export const createSlide = createAsyncThunk<
  Slide,
  { presentationId: string; data: CreateSlideRequest },
  { rejectValue: string }
>(
  'presentation/createSlide',
  async ({ presentationId, data }, { rejectWithValue }) => {
    try {
      const response = await presentationService.createSlide(presentationId, data)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to create slide'
      return rejectWithValue(message)
    }
  }
)

export const updateSlide = createAsyncThunk<
  Slide,
  { presentationId: string; slideId: string; data: UpdateSlideRequest },
  { rejectValue: string }
>(
  'presentation/updateSlide',
  async ({ presentationId, slideId, data }, { rejectWithValue }) => {
    try {
      const response = await presentationService.updateSlide(presentationId, slideId, data)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to update slide'
      return rejectWithValue(message)
    }
  }
)

export const deleteSlide = createAsyncThunk<
  string,
  { presentationId: string; slideId: string },
  { rejectValue: string }
>(
  'presentation/deleteSlide',
  async ({ presentationId, slideId }, { rejectWithValue }) => {
    try {
      await presentationService.deleteSlide(presentationId, slideId)
      return slideId
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to delete slide'
      return rejectWithValue(message)
    }
  }
)

export const duplicateSlide = createAsyncThunk<
  Slide,
  { presentationId: string; slideId: string },
  { rejectValue: string }
>(
  'presentation/duplicateSlide',
  async ({ presentationId, slideId }, { rejectWithValue }) => {
    try {
      const response = await presentationService.duplicateSlide(presentationId, slideId)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to duplicate slide'
      return rejectWithValue(message)
    }
  }
)

export const reorderSlides = createAsyncThunk<
  Slide[],
  { presentationId: string; slideOrder: { slide_id: string; position: number }[] },
  { rejectValue: string }
>(
  'presentation/reorderSlides',
  async ({ presentationId, slideOrder }, { rejectWithValue }) => {
    try {
      const response = await presentationService.reorderSlides(presentationId, slideOrder)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to reorder slides'
      return rejectWithValue(message)
    }
  }
)

// Search and filter
export const searchPresentations = createAsyncThunk<
  { presentations: Presentation[]; total: number; has_more: boolean },
  {
    search?: string
    tags?: string[]
    date_from?: string
    date_to?: string
    sort_by?: 'created_at' | 'updated_at' | 'title'
    sort_order?: 'asc' | 'desc'
    limit?: number
    offset?: number
  },
  { rejectValue: string }
>(
  'presentation/searchPresentations',
  async (query, { rejectWithValue }) => {
    try {
      const response = await presentationService.searchPresentations(query)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to search presentations'
      return rejectWithValue(message)
    }
  }
)

// Presentation slice
const presentationSlice = createSlice({
  name: 'presentation',
  initialState,
  reducers: {
    // Clear current presentation
    clearCurrentPresentation: (state) => {
      state.currentPresentation = null
    },
    
    // Clear errors
    clearError: (state) => {
      state.error = null
    },
    
    // Set loading state
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload
    },
    
    // Update current presentation
    updateCurrentPresentation: (state, action: PayloadAction<Partial<Presentation>>) => {
      if (state.currentPresentation) {
        state.currentPresentation = { ...state.currentPresentation, ...action.payload }
      }
    },
    
    // Add slide to current presentation
    addSlideToCurrentPresentation: (state, action: PayloadAction<Slide>) => {
      if (state.currentPresentation) {
        state.currentPresentation.slides.push(action.payload)
      }
    },
    
    // Update slide in current presentation
    updateSlideInCurrentPresentation: (state, action: PayloadAction<Slide>) => {
      if (state.currentPresentation) {
        const slideIndex = state.currentPresentation.slides.findIndex(
          slide => slide.id === action.payload.id
        )
        if (slideIndex !== -1) {
          state.currentPresentation.slides[slideIndex] = action.payload
        }
      }
    },
    
    // Remove slide from current presentation
    removeSlideFromCurrentPresentation: (state, action: PayloadAction<string>) => {
      if (state.currentPresentation) {
        state.currentPresentation.slides = state.currentPresentation.slides.filter(
          slide => slide.id !== action.payload
        )
      }
    },
    
    // Reset state
    resetState: (state) => {
      state.presentations = []
      state.currentPresentation = null
      state.isLoading = false
      state.error = null
    },
  },
  extraReducers: (builder) => {
    // Fetch presentations
    builder
      .addCase(fetchPresentations.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchPresentations.fulfilled, (state, action) => {
        state.isLoading = false
        state.presentations = action.payload
        state.error = null
      })
      .addCase(fetchPresentations.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to fetch presentations'
      })

    // Fetch single presentation
    builder
      .addCase(fetchPresentation.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchPresentation.fulfilled, (state, action) => {
        state.isLoading = false
        state.currentPresentation = action.payload
        state.error = null
      })
      .addCase(fetchPresentation.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to fetch presentation'
      })

    // Create presentation
    builder
      .addCase(createPresentation.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(createPresentation.fulfilled, (state, action) => {
        state.isLoading = false
        state.presentations.unshift(action.payload)
        state.currentPresentation = action.payload
        state.error = null
      })
      .addCase(createPresentation.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to create presentation'
      })

    // Update presentation
    builder
      .addCase(updatePresentation.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(updatePresentation.fulfilled, (state, action) => {
        state.isLoading = false
        const index = state.presentations.findIndex(p => p.id === action.payload.id)
        if (index !== -1) {
          state.presentations[index] = action.payload
        }
        if (state.currentPresentation?.id === action.payload.id) {
          state.currentPresentation = action.payload
        }
        state.error = null
      })
      .addCase(updatePresentation.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to update presentation'
      })

    // Delete presentation
    builder
      .addCase(deletePresentation.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(deletePresentation.fulfilled, (state, action) => {
        state.isLoading = false
        state.presentations = state.presentations.filter(p => p.id !== action.payload)
        if (state.currentPresentation?.id === action.payload) {
          state.currentPresentation = null
        }
        state.error = null
      })
      .addCase(deletePresentation.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to delete presentation'
      })

    // Duplicate presentation
    builder
      .addCase(duplicatePresentation.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(duplicatePresentation.fulfilled, (state, action) => {
        state.isLoading = false
        state.presentations.unshift(action.payload)
        state.error = null
      })
      .addCase(duplicatePresentation.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to duplicate presentation'
      })

    // Search presentations
    builder
      .addCase(searchPresentations.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(searchPresentations.fulfilled, (state, action) => {
        state.isLoading = false
        state.presentations = action.payload.presentations
        state.error = null
      })
      .addCase(searchPresentations.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to search presentations'
      })

    // Slide operations
    builder
      .addCase(createSlide.fulfilled, (state, action) => {
        if (state.currentPresentation) {
          state.currentPresentation.slides.push(action.payload)
        }
      })
      .addCase(updateSlide.fulfilled, (state, action) => {
        if (state.currentPresentation) {
          const slideIndex = state.currentPresentation.slides.findIndex(
            slide => slide.id === action.payload.id
          )
          if (slideIndex !== -1) {
            state.currentPresentation.slides[slideIndex] = action.payload
          }
        }
      })
      .addCase(deleteSlide.fulfilled, (state, action) => {
        if (state.currentPresentation) {
          state.currentPresentation.slides = state.currentPresentation.slides.filter(
            slide => slide.id !== action.payload
          )
        }
      })
      .addCase(duplicateSlide.fulfilled, (state, action) => {
        if (state.currentPresentation) {
          state.currentPresentation.slides.push(action.payload)
        }
      })
      .addCase(reorderSlides.fulfilled, (state, action) => {
        if (state.currentPresentation) {
          state.currentPresentation.slides = action.payload
        }
      })
  },
})

export const {
  clearCurrentPresentation,
  clearError,
  setLoading,
  updateCurrentPresentation,
  addSlideToCurrentPresentation,
  updateSlideInCurrentPresentation,
  removeSlideFromCurrentPresentation,
  resetState,
} = presentationSlice.actions

export default presentationSlice.reducer