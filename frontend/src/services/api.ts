/**
 * API Client for backend communication
 */
import axios, { AxiosInstance } from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

class APIClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add request interceptor to include auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized - redirect to login
          this.removeToken()
          if (typeof window !== 'undefined') {
            window.location.href = '/login'
          }
        }
        return Promise.reject(error)
      }
    )
  }

  private getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('access_token')
    }
    return null
  }

  private setToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token)
    }
  }

  private removeToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token')
    }
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)

    const response = await this.client.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    if (response.data.access_token) {
      this.setToken(response.data.access_token)
    }

    return response.data
  }

  async register(data: { email: string; password: string; full_name?: string; organization_name: string }) {
    const response = await this.client.post('/auth/register', data)
    return response.data
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me')
    return response.data
  }

  logout(): void {
    this.removeToken()
  }

  // Organizations
  async getOrganizations() {
    const response = await this.client.get('/organizations')
    return response.data
  }

  // AI Tools
  async getAITools() {
    const response = await this.client.get('/ai-tools')
    return response.data
  }

  async getAIToolROI(toolId: number) {
    const response = await this.client.get(`/ai-tools/${toolId}/roi`)
    return response.data
  }

  // Metrics
  async getMetrics() {
    const response = await this.client.get('/metrics')
    return response.data
  }

  // Analytics
  async getDashboardData(view: 'cfo' | 'chro' | 'cio' | 'department') {
    const response = await this.client.get('/analytics/dashboard', {
      params: { view },
    })
    return response.data
  }

  async getROISummary() {
    const response = await this.client.get('/analytics/roi-summary')
    return response.data
  }

  async getAttributionAnalysis(params?: { metric_id?: number; ai_tool_id?: number }) {
    const response = await this.client.get('/analytics/attribution', { params })
    return response.data
  }
}

export const apiClient = new APIClient()
