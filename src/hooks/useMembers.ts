import { useState, useEffect } from 'react';
import { Member, FilterType } from '../types/member';
import { MemberService } from '../services/memberService';
import toast from 'react-hot-toast';

export const useMembers = () => {
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<FilterType>('all');

  const loadMembers = async () => {
    try {
      setLoading(true);
      const data = await MemberService.getFilteredMembers(filter);
      setMembers(data);
    } catch (error) {
      toast.error('Failed to load members');
      console.error('Error loading members:', error);
    } finally {
      setLoading(false);
    }
  };

  const createMember = async (memberData: Omit<Member, 'id' | 'created_at' | 'updated_at'>) => {
    try {
      await MemberService.createMember(memberData);
      await loadMembers();
      toast.success('Member created successfully');
    } catch (error) {
      toast.error('Failed to create member');
      console.error('Error creating member:', error);
    }
  };

  const updateMember = async (id: string, updates: Partial<Member>) => {
    try {
      await MemberService.updateMember(id, updates);
      await loadMembers();
      toast.success('Member updated successfully');
    } catch (error) {
      toast.error('Failed to update member');
      console.error('Error updating member:', error);
    }
  };

  const deleteMember = async (id: string) => {
    try {
      await MemberService.deleteMember(id);
      await loadMembers();
      toast.success('Member deleted successfully');
    } catch (error) {
      toast.error('Failed to delete member');
      console.error('Error deleting member:', error);
    }
  };

  useEffect(() => {
    loadMembers();
  }, [filter]);

  return {
    members,
    loading,
    filter,
    setFilter,
    createMember,
    updateMember,
    deleteMember,
    refresh: loadMembers
  };
};