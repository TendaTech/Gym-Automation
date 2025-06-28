import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://placeholder.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'placeholder-key';

// Only create Supabase client if real credentials are provided
export const supabase = supabaseUrl !== 'https://placeholder.supabase.co' && supabaseAnonKey !== 'placeholder-key' 
  ? createClient(supabaseUrl, supabaseAnonKey)
  : null;

// For demo purposes, we'll use localStorage as a fallback
const STORAGE_KEY = 'gym_members';
const LOGS_STORAGE_KEY = 'gym_email_logs';

export const storageService = {
  getMembers: (): any[] => {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  },

  saveMembers: (members: any[]) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(members));
  },

  getLogs: (): any[] => {
    try {
      const data = localStorage.getItem(LOGS_STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  },

  saveLogs: (logs: any[]) => {
    localStorage.setItem(LOGS_STORAGE_KEY, JSON.stringify(logs));
  }
};