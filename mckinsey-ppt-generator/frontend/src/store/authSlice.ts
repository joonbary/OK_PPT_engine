import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { 
  AuthState, 
  User, 
  LoginRequest, 
  RegisterRequest, 
  AuthResponse 
} from '../types'
import { authService } from '../services/auth.service'

// Initial state
const initialState: AuthState = {
  user: null,
  token: null,
  isLoading: false,
  error: null,
}

// Async thunks
export const loginUser = createAsyncThunk<
  AuthResponse,
  LoginRequest,
  { rejectValue: string }
>(
  'auth/login',
  async (credentials, { rejectWithValue }) => {
    try {
      const response = await authService.login(credentials)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Login failed'
      return rejectWithValue(message)
    }
  }
)

export const registerUser = createAsyncThunk<
  User,
  RegisterRequest,
  { rejectValue: string }
>(
  'auth/register',
  async (userData, { rejectWithValue }) => {
    try {
      const response = await authService.register(userData)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Registration failed'
      return rejectWithValue(message)
    }
  }
)

export const getCurrentUser = createAsyncThunk<
  User,
  void,
  { rejectValue: string }
>(
  'auth/getCurrentUser',
  async (_, { rejectWithValue }) => {
    try {
      const response = await authService.getCurrentUser()
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to get user profile'
      return rejectWithValue(message)
    }
  }
)

export const updateUserProfile = createAsyncThunk<
  User,
  Partial<User>,
  { rejectValue: string }
>(
  'auth/updateProfile',
  async (userData, { rejectWithValue }) => {
    try {
      const response = await authService.updateProfile(userData)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to update profile'
      return rejectWithValue(message)
    }
  }
)

export const changePassword = createAsyncThunk<
  { message: string },
  { current_password: string; new_password: string },
  { rejectValue: string }
>(
  'auth/changePassword',
  async (passwordData, { rejectWithValue }) => {
    try {
      const response = await authService.changePassword(passwordData)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to change password'
      return rejectWithValue(message)
    }
  }
)

export const requestPasswordReset = createAsyncThunk<
  { message: string },
  string,
  { rejectValue: string }
>(
  'auth/requestPasswordReset',
  async (email, { rejectWithValue }) => {
    try {
      const response = await authService.requestPasswordReset(email)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to request password reset'
      return rejectWithValue(message)
    }
  }
)

export const resetPassword = createAsyncThunk<
  { message: string },
  { token: string; new_password: string },
  { rejectValue: string }
>(
  'auth/resetPassword',
  async (resetData, { rejectWithValue }) => {
    try {
      const response = await authService.resetPassword(resetData)
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to reset password'
      return rejectWithValue(message)
    }
  }
)

export const refreshToken = createAsyncThunk<
  AuthResponse,
  void,
  { rejectValue: string }
>(
  'auth/refreshToken',
  async (_, { rejectWithValue }) => {
    try {
      const response = await authService.refreshToken()
      return response
    } catch (error: any) {
      const message = error?.response?.data?.detail || 
                    error?.message || 
                    'Failed to refresh token'
      return rejectWithValue(message)
    }
  }
)

// Auth slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    // Initialize auth state from localStorage
    initializeAuth: (state) => {
      const { token, user } = authService.initializeAuth()
      state.token = token
      state.user = user
      state.isLoading = false
      state.error = null
    },
    
    // Clear auth state and localStorage
    logout: (state) => {
      authService.logout()
      state.user = null
      state.token = null
      state.isLoading = false
      state.error = null
    },
    
    // Clear errors
    clearError: (state) => {
      state.error = null
    },
    
    // Set loading state
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload
    },
    
    // Update user data
    updateUser: (state, action: PayloadAction<Partial<User>>) => {
      if (state.user) {
        state.user = { ...state.user, ...action.payload }
      }
    },
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoading = false
        state.user = action.payload.user
        state.token = action.payload.access_token
        state.error = null
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Login failed'
        state.user = null
        state.token = null
      })

    // Register
    builder
      .addCase(registerUser.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(registerUser.fulfilled, (state) => {
        state.isLoading = false
        state.error = null
        // Don't auto-login after registration
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Registration failed'
      })

    // Get current user
    builder
      .addCase(getCurrentUser.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(getCurrentUser.fulfilled, (state, action) => {
        state.isLoading = false
        state.user = action.payload
        state.error = null
      })
      .addCase(getCurrentUser.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to get user profile'
        // If getting current user fails, likely token is invalid
        if (action.payload?.includes('401') || action.payload?.includes('Unauthorized')) {
          state.user = null
          state.token = null
        }
      })

    // Update profile
    builder
      .addCase(updateUserProfile.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(updateUserProfile.fulfilled, (state, action) => {
        state.isLoading = false
        state.user = action.payload
        state.error = null
      })
      .addCase(updateUserProfile.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to update profile'
      })

    // Change password
    builder
      .addCase(changePassword.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(changePassword.fulfilled, (state) => {
        state.isLoading = false
        state.error = null
      })
      .addCase(changePassword.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to change password'
      })

    // Request password reset
    builder
      .addCase(requestPasswordReset.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(requestPasswordReset.fulfilled, (state) => {
        state.isLoading = false
        state.error = null
      })
      .addCase(requestPasswordReset.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to request password reset'
      })

    // Reset password
    builder
      .addCase(resetPassword.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(resetPassword.fulfilled, (state) => {
        state.isLoading = false
        state.error = null
      })
      .addCase(resetPassword.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to reset password'
      })

    // Refresh token
    builder
      .addCase(refreshToken.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(refreshToken.fulfilled, (state, action) => {
        state.isLoading = false
        state.token = action.payload.access_token
        if (action.payload.user) {
          state.user = action.payload.user
        }
        state.error = null
      })
      .addCase(refreshToken.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload || 'Failed to refresh token'
        // Clear auth state if refresh fails
        state.user = null
        state.token = null
      })
  },
})

export const {
  initializeAuth,
  logout,
  clearError,
  setLoading,
  updateUser,
} = authSlice.actions

export default authSlice.reducer