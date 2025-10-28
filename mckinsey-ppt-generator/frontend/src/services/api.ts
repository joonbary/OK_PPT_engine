import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { toast } from 'react-toastify'

// Types for API responses
export interface ApiResponse<T = any> {
  data: T
  message?: string
  status: number
}

export interface ApiError {
  detail: string
  status_code: number
}

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error: AxiosError<ApiError>) => {
    const { response } = error

    if (response) {
      const { status, data } = response

      switch (status) {
        case 401:
          // Unauthorized - redirect to login
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          window.location.href = '/auth/login'
          toast.error('Session expired. Please log in again.')
          break

        case 403:
          // Forbidden
          toast.error('You do not have permission to perform this action.')
          break

        case 404:
          // Not found
          toast.error('The requested resource was not found.')
          break

        case 422:
          // Validation error
          if (data?.detail) {
            if (Array.isArray(data.detail)) {
              // Handle FastAPI validation errors
              const validationErrors = data.detail
                .map((err: any) => `${err.loc.join('.')}: ${err.msg}`)
                .join(', ')
              toast.error(`Validation error: ${validationErrors}`)
            } else if (typeof data.detail === 'string') {
              toast.error(data.detail)
            }
          } else {
            toast.error('Validation error occurred.')
          }
          break

        case 429:
          // Rate limited
          toast.error('Too many requests. Please try again later.')
          break

        case 500:
          // Internal server error
          toast.error('Internal server error. Please try again later.')
          break

        case 502:
        case 503:
        case 504:
          // Server errors
          toast.error('Server is temporarily unavailable. Please try again later.')
          break

        default:
          // Other errors
          const errorMessage = data?.detail || `An error occurred (${status})`
          toast.error(errorMessage)
      }
    } else if (error.request) {
      // Network error
      toast.error('Network error. Please check your connection and try again.')
    } else {
      // Other error
      toast.error('An unexpected error occurred.')
    }

    return Promise.reject(error)
  }
)

// API helper functions
export const apiRequest = {
  get: async <T = any>(url: string, params?: any): Promise<T> => {
    const response = await api.get<T>(url, { params })
    return response.data
  },

  post: async <T = any>(url: string, data?: any): Promise<T> => {
    const response = await api.post<T>(url, data)
    return response.data
  },

  put: async <T = any>(url: string, data?: any): Promise<T> => {
    const response = await api.put<T>(url, data)
    return response.data
  },

  patch: async <T = any>(url: string, data?: any): Promise<T> => {
    const response = await api.patch<T>(url, data)
    return response.data
  },

  delete: async <T = any>(url: string): Promise<T> => {
    const response = await api.delete<T>(url)
    return response.data
  },
}

// File upload helper
export const uploadFile = async (
  url: string,
  file: File,
  fieldName: string = 'file',
  additionalData?: Record<string, any>,
  onProgress?: (progress: number) => void
): Promise<any> => {
  const formData = new FormData()
  formData.append(fieldName, file)

  // Add additional form data if provided
  if (additionalData) {
    Object.keys(additionalData).forEach((key) => {
      formData.append(key, additionalData[key])
    })
  }

  const response = await api.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress && progressEvent.total) {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(progress)
      }
    },
  })

  return response.data
}

// Download helper
export const downloadFile = async (
  url: string,
  filename?: string,
  params?: any
): Promise<void> => {
  try {
    const response = await api.get(url, {
      params,
      responseType: 'blob',
    })

    // Create blob link to download
    const blob = new Blob([response.data])
    const link = document.createElement('a')
    link.href = window.URL.createObjectURL(blob)

    // Set filename from response headers or use provided filename
    const contentDisposition = response.headers['content-disposition']
    let downloadFilename = filename

    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="(.+)"/)
      if (filenameMatch) {
        downloadFilename = filenameMatch[1]
      }
    }

    link.download = downloadFilename || 'download'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(link.href)
  } catch (error) {
    console.error('Download failed:', error)
    toast.error('Failed to download file')
  }
}

// Health check helper
export const checkApiHealth = async (): Promise<boolean> => {
  try {
    await api.get('/health')
    return true
  } catch (error) {
    return false
  }
}

export default api