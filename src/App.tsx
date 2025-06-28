import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { LoginPage } from './components/auth/LoginPage';
import { DashboardLayout } from './components/layout/DashboardLayout';
import { DashboardHome } from './components/dashboard/DashboardHome';
import { MemberProfile } from './components/members/MemberProfile';
import { MemberPortal } from './components/members/MemberPortal';
import { MemberTable } from './components/MemberTable';
import { AddMemberModal } from './components/members/AddMemberModal';
import { EmailLogsModal } from './components/EmailLogsModal';
import { BulkUploadModal } from './components/BulkUploadModal';
import { useMembers } from './hooks/useMembers';
import { Member } from './types/member';
import { EmailService, MemberService } from './services/memberService';
import { sampleMembers } from './data/sampleData';
import { storageService } from './lib/supabase';
import toast from 'react-hot-toast';
import { useState, useEffect } from 'react';
import { Plus, FileText, Upload } from 'lucide-react';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { currentUser } = useAuth();
  return currentUser ? <>{children}</> : <Navigate to="/login" />;
};

const MembersPage: React.FC = () => {
  const { members, loading, filter, setFilter, createMember, updateMember, deleteMember, refresh } = useMembers();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLogsModalOpen, setIsLogsModalOpen] = useState(false);
  const [isBulkUploadOpen, setIsBulkUploadOpen] = useState(false);
  const [editingMember, setEditingMember] = useState<Member | null>(null);
  const [modalMode, setModalMode] = useState<'create' | 'edit'>('create');
  const [isInitialized, setIsInitialized] = useState(false);
  const [isSendingReminders, setIsSendingReminders] = useState(false);

  // Initialize with sample data if no members exist
  useEffect(() => {
    const initializeData = async () => {
      const existingMembers = storageService.getMembers();
      if (existingMembers.length === 0) {
        storageService.saveMembers(sampleMembers);
        await refresh();
      }
      setIsInitialized(true);
    };

    if (!isInitialized) {
      initializeData();
    }
  }, [isInitialized, refresh]);

  const handleCreateMember = () => {
    setEditingMember(null);
    setModalMode('create');
    setIsModalOpen(true);
  };

  const handleEditMember = (member: Member) => {
    setEditingMember(member);
    setModalMode('edit');
    setIsModalOpen(true);
  };

  const handleDeleteMember = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this member?')) {
      await deleteMember(id);
    }
  };

  const handleModalSubmit = async (data: Omit<Member, 'id' | 'created_at' | 'updated_at'>) => {
    if (modalMode === 'create') {
      await createMember(data);
    } else if (editingMember) {
      await updateMember(editingMember.id, data);
    }
    setIsModalOpen(false);
  };

  const handleSendReminders = async () => {
    setIsSendingReminders(true);
    try {
      const result = await EmailService.sendSubscriptionReminders();
      toast.success(`Reminders sent! ${result.sent} successful, ${result.failed} failed`);
      
      // Also send motivational emails
      const motivationalResult = await EmailService.sendMotivationalEmails();
      if (motivationalResult.sent > 0) {
        toast.success(`${motivationalResult.sent} motivational emails sent!`);
      }
    } catch (error) {
      toast.error('Failed to send reminders');
      console.error('Error sending reminders:', error);
    } finally {
      setIsSendingReminders(false);
    }
  };

  const getCounts = async () => {
    const allMembers = await MemberService.getAllMembers();
    return {
      all: allMembers.length,
      due_soon: (await MemberService.getFilteredMembers('due_soon')).length,
      inactive: (await MemberService.getFilteredMembers('inactive')).length,
      birthdays: (await MemberService.getFilteredMembers('birthdays')).length,
      active_only: (await MemberService.getFilteredMembers('active_only')).length,
    };
  };

  const [counts, setCounts] = useState({
    all: 0,
    due_soon: 0,
    inactive: 0,
    birthdays: 0,
    active_only: 0,
  });

  useEffect(() => {
    const updateCounts = async () => {
      const newCounts = await getCounts();
      setCounts(newCounts);
    };
    
    if (isInitialized) {
      updateCounts();
    }
  }, [members, isInitialized]);

  if (!isInitialized) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Members</h1>
          <p className="text-gray-600 mt-1">Manage your gym members and their subscriptions</p>
        </div>
        
        <div className="flex space-x-3">
          <button
            onClick={() => setIsBulkUploadOpen(true)}
            className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
          >
            <Upload className="h-4 w-4 mr-2" />
            Bulk Upload
          </button>
          
          <button
            onClick={() => setIsLogsModalOpen(true)}
            className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
          >
            <FileText className="h-4 w-4 mr-2" />
            View Logs
          </button>
          
          <button
            onClick={handleCreateMember}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
          >
            <Plus className="h-4 w-4 mr-2" />
            Add Member
          </button>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
        </div>
      ) : (
        <MemberTable 
          members={members}
          onEdit={handleEditMember}
          onDelete={handleDeleteMember}
        />
      )}

      <AddMemberModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleModalSubmit}
      />

      <EmailLogsModal
        isOpen={isLogsModalOpen}
        onClose={() => setIsLogsModalOpen(false)}
      />

      <BulkUploadModal
        isOpen={isBulkUploadOpen}
        onClose={() => setIsBulkUploadOpen(false)}
        onSuccess={refresh}
      />
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Toaster position="top-right" />
          
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<Navigate to="/dashboard" />} />
            
            <Route path="/*" element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }>
              <Route path="dashboard" element={<DashboardHome />} />
              <Route path="members" element={<MembersPage />} />
              <Route path="members/:id" element={<MemberProfile />} />
              <Route path="portal" element={<MemberPortal />} />
              <Route path="schedule" element={<div className="p-6"><h1 className="text-2xl font-bold">Schedule</h1><p className="text-gray-600 mt-2">Schedule management coming soon...</p></div>} />
              <Route path="settings" element={<div className="p-6"><h1 className="text-2xl font-bold">Settings</h1><p className="text-gray-600 mt-2">Settings panel coming soon...</p></div>} />
            </Route>
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;