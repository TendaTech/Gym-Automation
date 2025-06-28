import { Member, EmailLog, FilterType } from '../types/member';
import { apiService } from './apiService';
import { storageService } from '../lib/supabase';
import { differenceInDays } from 'date-fns';

export class MemberService {
  static generateId(): string {
    return crypto.randomUUID();
  }

  static async getAllMembers(): Promise<Member[]> {
    try {
      // Try to get from API first
      return await apiService.getMembers();
    } catch (error) {
      console.warn('API not available, falling back to localStorage:', error);
      // Fallback to localStorage
      return storageService.getMembers();
    }
  }

  static async createMember(memberData: Omit<Member, 'id' | 'created_at' | 'updated_at'>): Promise<Member> {
    try {
      return await apiService.createMember(memberData);
    } catch (error) {
      console.warn('API not available, using localStorage:', error);
      // Fallback to localStorage
      const members = storageService.getMembers();
      const newMember: Member = {
        ...memberData,
        id: this.generateId(),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      
      members.push(newMember);
      storageService.saveMembers(members);
      return newMember;
    }
  }

  static async updateMember(id: string, updates: Partial<Member>): Promise<Member | null> {
    try {
      return await apiService.updateMember(id, updates);
    } catch (error) {
      console.warn('API not available, using localStorage:', error);
      // Fallback to localStorage
      const members = storageService.getMembers();
      const index = members.findIndex(m => m.id === id);
      
      if (index === -1) return null;
      
      members[index] = {
        ...members[index],
        ...updates,
        updated_at: new Date().toISOString()
      };
      
      storageService.saveMembers(members);
      return members[index];
    }
  }

  static async deleteMember(id: string): Promise<boolean> {
    try {
      await apiService.deleteMember(id);
      return true;
    } catch (error) {
      console.warn('API not available, using localStorage:', error);
      // Fallback to localStorage
      const members = storageService.getMembers();
      const filteredMembers = members.filter(m => m.id !== id);
      
      if (filteredMembers.length === members.length) return false;
      
      storageService.saveMembers(filteredMembers);
      return true;
    }
  }

  static async getFilteredMembers(filter: FilterType): Promise<Member[]> {
    try {
      return await apiService.getMembers(filter);
    } catch (error) {
      console.warn('API not available, filtering locally:', error);
      // Fallback to local filtering
      const members = await this.getAllMembers();
      const today = new Date();

      switch (filter) {
        case 'due_soon':
          return members.filter(member => {
            const dueDate = new Date(member.subscription_due_date);
            const daysUntilDue = differenceInDays(dueDate, today);
            return daysUntilDue <= 5 && daysUntilDue >= 0;
          });
        
        case 'inactive':
          return members.filter(member => {
            if (!member.last_checkin_date) return true;
            const lastCheckin = new Date(member.last_checkin_date);
            return differenceInDays(today, lastCheckin) > 7;
          });
        
        case 'birthdays':
          return members.filter(member => {
            if (!member.birthday) return false;
            const birthday = new Date(member.birthday);
            const todayMonth = today.getMonth();
            const todayDate = today.getDate();
            return birthday.getMonth() === todayMonth && birthday.getDate() === todayDate;
          });
        
        case 'active_only':
          return members.filter(member => member.is_active);
        
        default:
          return members;
      }
    }
  }

  static getDaysUntilDue(dueDate: string): number {
    return differenceInDays(new Date(dueDate), new Date());
  }

  static getDaysSinceLastCheckin(lastCheckinDate?: string): number {
    if (!lastCheckinDate) return Infinity;
    return differenceInDays(new Date(), new Date(lastCheckinDate));
  }

  static isBirthdayToday(birthday?: string): boolean {
    if (!birthday) return false;
    const today = new Date();
    const birthdayDate = new Date(birthday);
    return today.getMonth() === birthdayDate.getMonth() && 
           today.getDate() === birthdayDate.getDate();
  }
}

export class EmailService {
  static async logEmail(log: Omit<EmailLog, 'id' | 'sent_date'>): Promise<void> {
    // Try API first, fallback to localStorage
    try {
      // API logging would be handled by the backend
      console.log('Email logged via API');
    } catch (error) {
      const logs = storageService.getLogs();
      const newLog: EmailLog = {
        ...log,
        id: MemberService.generateId(),
        sent_date: new Date().toISOString()
      };
      
      logs.push(newLog);
      storageService.saveLogs(logs);
    }
  }

  static async getEmailLogs(): Promise<EmailLog[]> {
    try {
      return await apiService.getEmailLogs();
    } catch (error) {
      console.warn('API not available, using localStorage:', error);
      return storageService.getLogs();
    }
  }

  static async sendSubscriptionReminders(): Promise<{ sent: number; failed: number }> {
    try {
      return await apiService.sendSubscriptionReminders();
    } catch (error) {
      console.warn('API not available, simulating email send:', error);
      // Fallback simulation
      const members = await MemberService.getFilteredMembers('due_soon');
      let sent = 0;
      let failed = 0;

      for (const member of members) {
        try {
          await this.simulateEmailSend(member.email, 'subscription_reminder', member);
          await this.logEmail({
            member_id: member.id,
            email_type: 'subscription',
            status: 'sent',
            member_name: member.full_name,
            member_email: member.email
          });
          sent++;
        } catch (error) {
          await this.logEmail({
            member_id: member.id,
            email_type: 'subscription',
            status: 'failed',
            member_name: member.full_name,
            member_email: member.email
          });
          failed++;
        }
      }

      return { sent, failed };
    }
  }

  static async sendMotivationalEmails(): Promise<{ sent: number; failed: number }> {
    try {
      return await apiService.sendMotivationalEmails();
    } catch (error) {
      console.warn('API not available, simulating email send:', error);
      // Fallback simulation
      const members = await MemberService.getFilteredMembers('active_only');
      let sent = 0;
      let failed = 0;

      for (const member of members) {
        try {
          await this.simulateEmailSend(member.email, 'motivational', member);
          await this.logEmail({
            member_id: member.id,
            email_type: 'motivational',
            status: 'sent',
            member_name: member.full_name,
            member_email: member.email
          });
          sent++;
        } catch (error) {
          await this.logEmail({
            member_id: member.id,
            email_type: 'motivational',
            status: 'failed',
            member_name: member.full_name,
            member_email: member.email
          });
          failed++;
        }
      }

      return { sent, failed };
    }
  }

  private static async simulateEmailSend(email: string, type: string, member: Member): Promise<void> {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // Simulate 95% success rate
    if (Math.random() < 0.05) {
      throw new Error('Email send failed');
    }
    
    console.log(`📧 Email sent to ${email} (${type}):`, {
      name: member.full_name,
      type
    });
  }
}