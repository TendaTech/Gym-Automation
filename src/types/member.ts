export interface Member {
  id: string;
  full_name: string;
  email: string;
  phone?: string;
  subscription_due_date: string;
  birthday?: string;
  last_checkin_date?: string;
  emergency_contact?: string;
  address?: string;
  membership_type?: string;
  notes?: string;
  milestones?: string[];
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface EmailLog {
  id: string;
  member_id: string;
  email_type: 'subscription' | 'inactivity' | 'birthday' | 'motivational';
  sent_date: string;
  status: 'sent' | 'failed';
  member_name: string;
  member_email: string;
}

export type FilterType = 'all' | 'due_soon' | 'inactive' | 'birthdays' | 'active_only';