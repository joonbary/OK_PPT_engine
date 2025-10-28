import { apiRequest } from './api'
import { 
  LoginRequest, 
  RegisterRequest, 
  AuthResponse, 
  User 
} from '../types'

export class AuthService {
  private static instance: AuthService
  private readonly baseUrl = '/api/v1/auth'

  private constructor() {}

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService()
    }
    return AuthService.instance
  }

  /**
   * Login user with email and password
   */
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    try {
      // Format the request as form data for OAuth2 compatibility
      const formData = new FormData()
      formData.append('username', credentials.email) // OAuth2 uses 'username' field
      formData.append('password', credentials.password)

      const response = await apiRequest.post<AuthResponse>(
        `${this.baseUrl}/login`,
        formData,
      )

      // Store token and user in localStorage
      if (response.access_token) {
        this.setToken(response.access_token)
        this.setUser(response.user)
      }

      return response
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  /**
   * Register new user
   */
  async register(userData: RegisterRequest): Promise<User> {
    try {
      const response = await apiRequest.post<User>(
        `${this.baseUrl}/register`,
        userData
      )
      return response
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    }
  }

  /**
   * Get current user profile
   */
  async getCurrentUser(): Promise<User> {
    try {
      const response = await apiRequest.get<User>(`${this.baseUrl}/me`)
      this.setUser(response)
      return response
    } catch (error) {
      console.error('Get current user error:', error)
      throw error
    }
  }

  /**
   * Update user profile
   */
  async updateProfile(userData: Partial<User>): Promise<User> {
    try {
      const response = await apiRequest.put<User>(
        `${this.baseUrl}/me`,
        userData
      )
      this.setUser(response)
      return response
    } catch (error) {
      console.error('Update profile error:', error)
      throw error
    }
  }

  /**
   * Change user password
   */
  async changePassword(data: {
    current_password: string
    new_password: string
  }): Promise<{ message: string }> {
    try {
      const response = await apiRequest.put<{ message: string }>(
        `${this.baseUrl}/change-password`,
        data
      )
      return response
    } catch (error) {
      console.error('Change password error:', error)
      throw error
    }
  }

  /**
   * Request password reset
   */
  async requestPasswordReset(email: string): Promise<{ message: string }> {
    try {
      const response = await apiRequest.post<{ message: string }>(
        `${this.baseUrl}/password-reset/request`,
        { email }
      )
      return response
    } catch (error) {
      console.error('Password reset request error:', error)
      throw error
    }
  }

  /**
   * Reset password with token
   */
  async resetPassword(data: {
    token: string
    new_password: string
  }): Promise<{ message: string }> {
    try {
      const response = await apiRequest.post<{ message: string }>(
        `${this.baseUrl}/password-reset/confirm`,
        data
      )
      return response
    } catch (error) {
      console.error('Password reset error:', error)
      throw error
    }
  }

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<AuthResponse> {
    try {
      const response = await apiRequest.post<AuthResponse>(
        `${this.baseUrl}/refresh`
      )

      if (response.access_token) {
        this.setToken(response.access_token)
      }

      return response
    } catch (error) {
      console.error('Token refresh error:', error)
      // If refresh fails, clear stored data
      this.clearAuthData()
      throw error
    }
  }

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    try {
      // Call logout endpoint if available
      await apiRequest.post(`${this.baseUrl}/logout`)
    } catch (error) {
      console.error('Logout error:', error)
      // Continue with local logout even if API call fails
    } finally {
      this.clearAuthData()
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = this.getToken()
    if (!token) return false

    try {
      // Check if token is expired
      const payload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Date.now() / 1000
      return payload.exp > currentTime
    } catch (error) {
      console.error('Token validation error:', error)
      return false
    }
  }

  /**
   * Get stored token
   */
  getToken(): string | null {
    return localStorage.getItem('token')
  }

  /**
   * Get stored user
   */
  getUser(): User | null {
    const userStr = localStorage.getItem('user')
    if (!userStr) return null

    try {
      return JSON.parse(userStr) as User
    } catch (error) {
      console.error('Parse user error:', error)
      return null
    }
  }

  /**
   * Set token in localStorage
   */
  private setToken(token: string): void {
    localStorage.setItem('token', token)
  }

  /**
   * Set user in localStorage
   */
  private setUser(user: User): void {
    localStorage.setItem('user', JSON.stringify(user))
  }

  /**
   * Clear all authentication data
   */
  private clearAuthData(): void {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  /**
   * Initialize auth state from localStorage
   */
  initializeAuth(): { token: string | null; user: User | null } {
    const token = this.getToken()
    const user = this.getUser()

    // Validate token if it exists
    if (token && !this.isAuthenticated()) {
      this.clearAuthData()
      return { token: null, user: null }
    }

    return { token, user }
  }
}

// Export singleton instance
export const authService = AuthService.getInstance()
export default authService