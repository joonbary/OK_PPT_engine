// Authentication types
export interface User {
  id: string;
  email: string;
  full_name: string;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Presentation types
export interface Slide {
  id: string;
  presentation_id: string;
  slide_number: number;
  title: string;
  content: string;
  layout_type: string;
  created_at: string;
  updated_at: string;
}

export interface Presentation {
  id: string;
  title: string;
  description: string;
  user_id: string;
  slides: Slide[];
  created_at: string;
  updated_at: string;
}

export interface CreatePresentationRequest {
  title: string;
  description: string;
}

export interface UpdatePresentationRequest {
  title?: string;
  description?: string;
}

export interface CreateSlideRequest {
  title: string;
  content: string;
  layout_type: string;
  slide_number: number;
}

export interface UpdateSlideRequest {
  title?: string;
  content?: string;
  layout_type?: string;
  slide_number?: number;
}

// UI state types
export interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}

export interface PresentationState {
  presentations: Presentation[];
  currentPresentation: Presentation | null;
  isLoading: boolean;
  error: string | null;
}

// Layout types
export type SlideLayoutType = 
  | 'title_slide' 
  | 'content_slide' 
  | 'two_column' 
  | 'bullet_points' 
  | 'chart_slide' 
  | 'image_slide' 
  | 'conclusion_slide';

// API response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

// Form types
export interface FormFieldProps {
  name: string;
  label: string;
  type?: string;
  required?: boolean;
  multiline?: boolean;
  rows?: number;
}

// Theme types
export interface ThemeColors {
  primary: string;
  secondary: string;
  background: string;
  surface: string;
  text: string;
  textSecondary: string;
  error: string;
  warning: string;
  success: string;
}

export interface BreakpointValues {
  xs: number;
  sm: number;
  md: number;
  lg: number;
  xl: number;
}