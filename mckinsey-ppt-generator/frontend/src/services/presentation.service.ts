import { apiRequest, downloadFile, uploadFile } from './api'
import {
  Presentation,
  Slide,
  CreatePresentationRequest,
  UpdatePresentationRequest,
  CreateSlideRequest,
  UpdateSlideRequest,
} from '../types'

export class PresentationService {
  private static instance: PresentationService
  private readonly baseUrl = '/api/v1/presentations'

  private constructor() {}

  public static getInstance(): PresentationService {
    if (!PresentationService.instance) {
      PresentationService.instance = new PresentationService()
    }
    return PresentationService.instance
  }

  /**
   * Get all presentations for the current user
   */
  async getPresentations(): Promise<Presentation[]> {
    try {
      const response = await apiRequest.get<Presentation[]>(this.baseUrl)
      return response
    } catch (error) {
      console.error('Get presentations error:', error)
      throw error
    }
  }

  /**
   * Get a specific presentation by ID
   */
  async getPresentation(id: string): Promise<Presentation> {
    try {
      const response = await apiRequest.get<Presentation>(`${this.baseUrl}/${id}`)
      return response
    } catch (error) {
      console.error('Get presentation error:', error)
      throw error
    }
  }

  /**
   * Create a new presentation
   */
  async createPresentation(data: CreatePresentationRequest): Promise<Presentation> {
    try {
      const response = await apiRequest.post<Presentation>(this.baseUrl, data)
      return response
    } catch (error) {
      console.error('Create presentation error:', error)
      throw error
    }
  }

  /**
   * Update an existing presentation
   */
  async updatePresentation(
    id: string,
    data: UpdatePresentationRequest
  ): Promise<Presentation> {
    try {
      const response = await apiRequest.put<Presentation>(
        `${this.baseUrl}/${id}`,
        data
      )
      return response
    } catch (error) {
      console.error('Update presentation error:', error)
      throw error
    }
  }

  /**
   * Delete a presentation
   */
  async deletePresentation(id: string): Promise<{ message: string }> {
    try {
      const response = await apiRequest.delete<{ message: string }>(
        `${this.baseUrl}/${id}`
      )
      return response
    } catch (error) {
      console.error('Delete presentation error:', error)
      throw error
    }
  }

  /**
   * Duplicate a presentation
   */
  async duplicatePresentation(id: string): Promise<Presentation> {
    try {
      const response = await apiRequest.post<Presentation>(
        `${this.baseUrl}/${id}/duplicate`
      )
      return response
    } catch (error) {
      console.error('Duplicate presentation error:', error)
      throw error
    }
  }

  /**
   * Get slides for a specific presentation
   */
  async getSlides(presentationId: string): Promise<Slide[]> {
    try {
      const response = await apiRequest.get<Slide[]>(
        `${this.baseUrl}/${presentationId}/slides`
      )
      return response
    } catch (error) {
      console.error('Get slides error:', error)
      throw error
    }
  }

  /**
   * Get a specific slide
   */
  async getSlide(presentationId: string, slideId: string): Promise<Slide> {
    try {
      const response = await apiRequest.get<Slide>(
        `${this.baseUrl}/${presentationId}/slides/${slideId}`
      )
      return response
    } catch (error) {
      console.error('Get slide error:', error)
      throw error
    }
  }

  /**
   * Create a new slide
   */
  async createSlide(
    presentationId: string,
    data: CreateSlideRequest
  ): Promise<Slide> {
    try {
      const response = await apiRequest.post<Slide>(
        `${this.baseUrl}/${presentationId}/slides`,
        data
      )
      return response
    } catch (error) {
      console.error('Create slide error:', error)
      throw error
    }
  }

  /**
   * Update an existing slide
   */
  async updateSlide(
    presentationId: string,
    slideId: string,
    data: UpdateSlideRequest
  ): Promise<Slide> {
    try {
      const response = await apiRequest.put<Slide>(
        `${this.baseUrl}/${presentationId}/slides/${slideId}`,
        data
      )
      return response
    } catch (error) {
      console.error('Update slide error:', error)
      throw error
    }
  }

  /**
   * Delete a slide
   */
  async deleteSlide(
    presentationId: string,
    slideId: string
  ): Promise<{ message: string }> {
    try {
      const response = await apiRequest.delete<{ message: string }>(
        `${this.baseUrl}/${presentationId}/slides/${slideId}`
      )
      return response
    } catch (error) {
      console.error('Delete slide error:', error)
      throw error
    }
  }

  /**
   * Duplicate a slide
   */
  async duplicateSlide(presentationId: string, slideId: string): Promise<Slide> {
    try {
      const response = await apiRequest.post<Slide>(
        `${this.baseUrl}/${presentationId}/slides/${slideId}/duplicate`
      )
      return response
    } catch (error) {
      console.error('Duplicate slide error:', error)
      throw error
    }
  }

  /**
   * Reorder slides
   */
  async reorderSlides(
    presentationId: string,
    slideOrder: { slide_id: string; position: number }[]
  ): Promise<Slide[]> {
    try {
      const response = await apiRequest.put<Slide[]>(
        `${this.baseUrl}/${presentationId}/slides/reorder`,
        { slide_order: slideOrder }
      )
      return response
    } catch (error) {
      console.error('Reorder slides error:', error)
      throw error
    }
  }

  /**
   * Generate presentation from template
   */
  async generateFromTemplate(data: {
    template_id: string
    title: string
    description: string
    content_outline: string[]
  }): Promise<Presentation> {
    try {
      const response = await apiRequest.post<Presentation>(
        `${this.baseUrl}/generate`,
        data
      )
      return response
    } catch (error) {
      console.error('Generate from template error:', error)
      throw error
    }
  }

  /**
   * Export presentation to PowerPoint
   */
  async exportToPowerPoint(
    presentationId: string,
    options?: {
      include_notes?: boolean
      template_style?: string
      export_format?: 'pptx' | 'pdf'
    }
  ): Promise<void> {
    try {
      await downloadFile(
        `${this.baseUrl}/${presentationId}/export`,
        `presentation-${presentationId}.pptx`,
        options
      )
    } catch (error) {
      console.error('Export to PowerPoint error:', error)
      throw error
    }
  }

  /**
   * Import presentation from file
   */
  async importPresentation(
    file: File,
    options?: {
      preserve_formatting?: boolean
      extract_content_only?: boolean
    },
    onProgress?: (progress: number) => void
  ): Promise<Presentation> {
    try {
      const response = await uploadFile(
        `${this.baseUrl}/import`,
        file,
        'file',
        options,
        onProgress
      )
      return response
    } catch (error) {
      console.error('Import presentation error:', error)
      throw error
    }
  }

  /**
   * Get presentation analytics
   */
  async getPresentationAnalytics(presentationId: string): Promise<{
    views: number
    last_viewed: string
    time_spent: number
    slide_engagement: { slide_id: string; time_spent: number }[]
  }> {
    try {
      const response = await apiRequest.get(
        `${this.baseUrl}/${presentationId}/analytics`
      )
      return response
    } catch (error) {
      console.error('Get presentation analytics error:', error)
      throw error
    }
  }

  /**
   * Share presentation
   */
  async sharePresentation(
    presentationId: string,
    data: {
      share_type: 'public' | 'private'
      permissions: 'view' | 'edit'
      expires_at?: string
      password?: string
    }
  ): Promise<{
    share_url: string
    share_token: string
    expires_at: string
  }> {
    try {
      const response = await apiRequest.post(
        `${this.baseUrl}/${presentationId}/share`,
        data
      )
      return response
    } catch (error) {
      console.error('Share presentation error:', error)
      throw error
    }
  }

  /**
   * Get shared presentation (public access)
   */
  async getSharedPresentation(shareToken: string): Promise<Presentation> {
    try {
      const response = await apiRequest.get<Presentation>(
        `/api/v1/shared/presentations/${shareToken}`
      )
      return response
    } catch (error) {
      console.error('Get shared presentation error:', error)
      throw error
    }
  }

  /**
   * Search presentations
   */
  async searchPresentations(query: {
    search?: string
    tags?: string[]
    date_from?: string
    date_to?: string
    sort_by?: 'created_at' | 'updated_at' | 'title'
    sort_order?: 'asc' | 'desc'
    limit?: number
    offset?: number
  }): Promise<{
    presentations: Presentation[]
    total: number
    has_more: boolean
  }> {
    try {
      const response = await apiRequest.get(`${this.baseUrl}/search`, query)
      return response
    } catch (error) {
      console.error('Search presentations error:', error)
      throw error
    }
  }

  /**
   * Add image to slide
   */
  async addImageToSlide(
    presentationId: string,
    slideId: string,
    imageFile: File,
    position?: { x: number; y: number; width: number; height: number },
    onProgress?: (progress: number) => void
  ): Promise<{ image_url: string; image_id: string }> {
    try {
      const response = await uploadFile(
        `${this.baseUrl}/${presentationId}/slides/${slideId}/images`,
        imageFile,
        'image',
        { position },
        onProgress
      )
      return response
    } catch (error) {
      console.error('Add image to slide error:', error)
      throw error
    }
  }
}

// Export singleton instance
export const presentationService = PresentationService.getInstance()
export default presentationService