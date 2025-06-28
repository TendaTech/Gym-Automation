import { Member, EmailLog, FilterType } from '../types/member';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/members/api';

class ApiService {
  private getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  private async handleResponse(response: Response) {
    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Network error' }));
      throw new Error(error.message || `HTTP ${response.status}`);
    }
    return response.json();
  }

  // Authentication
  async login(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL.replace('/api/members/api', '')}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    return this.handleResponse(response);
  }

  async register(userData: any) {
    const response = await fetch(`${API_BASE_URL.replace('/api/members/api', '')}/auth/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return this.handleResponse(response);
  }

  // Members
  async getMembers(filter?: FilterType): Promise<Member[]> {
    const url = new URL(`${API_BASE_URL}/members/`);
    if (filter && filter !== 'all') {
      url.searchParams.append('filter', filter);
    }
    
    const response = await fetch(url.toString(), {
      headers: this.getAuthHeaders()
    });
    const data = await this.handleResponse(response);
    return data.results || data;
  }

  async getMember(id: string): Promise<Member> {
    const response = await fetch(`${API_BASE_URL}/members/${id}/`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  async createMember(memberData: Omit<Member, 'id' | 'created_at' | 'updated_at'>): Promise<Member> {
    const response = await fetch(`${API_BASE_URL}/members/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(memberData)
    });
    return this.handleResponse(response);
  }

  async updateMember(id: string, updates: Partial<Member>): Promise<Member> {
    const response = await fetch(`${API_BASE_URL}/members/${id}/`, {
      method: 'PATCH',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(updates)
    });
    return this.handleResponse(response);
  }

  async deleteMember(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/members/${id}/`, {
      method: 'DELETE',
      headers: this.getAuthHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete member');
    }
  }

  async getMemberStats() {
    const response = await fetch(`${API_BASE_URL}/members/stats/`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  async getMemberDashboard(memberId: string) {
    const response = await fetch(`${API_BASE_URL}/members/${memberId}/dashboard/`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  // Member Portal
  async getMemberPortalDashboard() {
    const response = await fetch(`${API_BASE_URL}/portal/dashboard/`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  // Coaches
  async getCoaches() {
    const response = await fetch(`${API_BASE_URL}/coaches/`, {
      headers: this.getAuthHeaders()
    });
    const data = await this.handleResponse(response);
    return data.results || data;
  }

  async getCoach(id: string) {
    const response = await fetch(`${API_BASE_URL}/coaches/${id}/`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  async getCoachSchedule(coachId: string) {
    const response = await fetch(`${API_BASE_URL}/coaches/${coachId}/schedule/`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  async getAvailableCoaches(date?: string) {
    const url = new URL(`${API_BASE_URL}/coaches/available/`);
    if (date) {
      url.searchParams.append('date', date);
    }
    
    const response = await fetch(url.toString(), {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  // Workout Plans
  async getWorkoutPlans() {
    const response = await fetch(`${API_BASE_URL}/workout-plans/`, {
      headers: this.getAuthHeaders()
    });
    const data = await this.handleResponse(response);
    return data.results || data;
  }

  async getWorkoutPlan(id: string) {
    const response = await fetch(`${API_BASE_URL}/workout-plans/${id}/`, {
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  // Workout Logs
  async getWorkoutLogs(memberId?: string) {
    const url = new URL(`${API_BASE_URL}/workout-logs/`);
    if (memberId) {
      url.searchParams.append('member', memberId);
    }
    
    const response = await fetch(url.toString(), {
      headers: this.getAuthHeaders()
    });
    const data = await this.handleResponse(response);
    return data.results || data;
  }

  async logWorkout(workoutData: any) {
    const response = await fetch(`${API_BASE_URL}/workout-logs/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(workoutData)
    });
    return this.handleResponse(response);
  }

  // Training Sessions
  async getTrainingSessions() {
    const response = await fetch(`${API_BASE_URL}/training-sessions/`, {
      headers: this.getAuthHeaders()
    });
    const data = await this.handleResponse(response);
    return data.results || data;
  }

  async joinTrainingSession(sessionId: string) {
    const response = await fetch(`${API_BASE_URL}/training-sessions/${sessionId}/join/`, {
      method: 'POST',
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  async leaveTrainingSession(sessionId: string) {
    const response = await fetch(`${API_BASE_URL}/training-sessions/${sessionId}/leave/`, {
      method: 'POST',
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  // Check-ins
  async checkin() {
    const response = await fetch(`${API_BASE_URL}/checkins/checkin/`, {
      method: 'POST',
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  async checkout() {
    const response = await fetch(`${API_BASE_URL}/checkins/checkout/`, {
      method: 'POST',
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  // Email Management
  async getEmailLogs(): Promise<EmailLog[]> {
    const response = await fetch(`${API_BASE_URL}/emails/logs/`, {
      headers: this.getAuthHeaders()
    });
    const data = await this.handleResponse(response);
    return data.results || data;
  }

  async sendEmails(emailData: any) {
    const response = await fetch(`${API_BASE_URL}/emails/send/`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(emailData)
    });
    return this.handleResponse(response);
  }

  async sendSubscriptionReminders() {
    const response = await fetch(`${API_BASE_URL}/emails/send-reminders/`, {
      method: 'POST',
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  async sendMotivationalEmails() {
    const response = await fetch(`${API_BASE_URL}/emails/send-motivational/`, {
      method: 'POST',
      headers: this.getAuthHeaders()
    });
    return this.handleResponse(response);
  }

  // Bulk Upload
  async bulkUploadMembers(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    
    const token = localStorage.getItem('access_token');
    const headers: Record<string, string> = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    const response = await fetch(`${API_BASE_URL}/members/bulk_upload/`, {
      method: 'POST',
      headers,
      body: formData
    });
    return this.handleResponse(response);
  }
}

export const apiService = new ApiService();