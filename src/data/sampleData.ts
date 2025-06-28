import { Member } from '../types/member';

export const sampleMembers: Member[] = [
  {
    id: '1',
    full_name: 'Sarah Johnson',
    email: 'sarah.johnson@email.com',
    subscription_due_date: '2024-12-20',
    birthday: '1992-03-15',
    last_checkin_date: '2024-12-10',
    milestones: ['Lost 15kg', 'Completed first marathon', '50 consecutive push-ups'],
    is_active: true,
    created_at: '2024-01-15T10:00:00Z',
    updated_at: '2024-12-10T14:30:00Z'
  },
  {
    id: '2',
    full_name: 'Mike Chen',
    email: 'mike.chen@email.com',
    subscription_due_date: '2024-12-18',
    birthday: '1988-07-22',
    last_checkin_date: '2024-12-05',
    milestones: ['Deadlift 200kg', 'Lost 20kg'],
    is_active: true,
    created_at: '2024-02-01T09:15:00Z',
    updated_at: '2024-12-05T16:45:00Z'
  },
  {
    id: '3',
    full_name: 'Emma Rodriguez',
    email: 'emma.rodriguez@email.com',
    subscription_due_date: '2024-12-15',
    birthday: '1995-12-14',
    last_checkin_date: '2024-11-28',
    milestones: ['First pull-up', 'Yoga instructor certification'],
    is_active: true,
    created_at: '2024-03-10T11:20:00Z',
    updated_at: '2024-11-28T18:15:00Z'
  },
  {
    id: '4',
    full_name: 'David Park',
    email: 'david.park@email.com',
    subscription_due_date: '2025-01-10',
    birthday: '1990-09-08',
    is_active: false,
    created_at: '2024-04-05T13:45:00Z',
    updated_at: '2024-11-15T12:00:00Z'
  },
  {
    id: '5',
    full_name: 'Lisa Thompson',
    email: 'lisa.thompson@email.com',
    subscription_due_date: '2024-12-25',
    birthday: '1987-12-14',
    last_checkin_date: '2024-12-12',
    milestones: ['Bench press bodyweight', '5K under 25 minutes', 'Lost 25kg'],
    is_active: true,
    created_at: '2024-05-20T15:30:00Z',
    updated_at: '2024-12-12T20:10:00Z'
  }
];