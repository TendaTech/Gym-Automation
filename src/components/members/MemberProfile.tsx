import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Edit, 
  Mail, 
  Phone, 
  Calendar, 
  MapPin, 
  Trophy, 
  Activity, 
  CreditCard,
  Camera,
  Save,
  X
} from 'lucide-react';
import { Member } from '../../types/member';
import { MemberService } from '../../services/memberService';
import { format } from 'date-fns';
import toast from 'react-hot-toast';

export const MemberProfile: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [member, setMember] = useState<Member | null>(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [editData, setEditData] = useState<Partial<Member>>({});

  useEffect(() => {
    loadMember();
  }, [id]);

  const loadMember = async () => {
    if (!id) return;
    
    try {
      const members = await MemberService.getAllMembers();
      const foundMember = members.find(m => m.id === id);
      if (foundMember) {
        setMember(foundMember);
        setEditData(foundMember);
      } else {
        toast.error('Member not found');
        navigate('/members');
      }
    } catch (error) {
      toast.error('Failed to load member');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!member || !id) return;
    
    try {
      await MemberService.updateMember(id, editData);
      setMember({ ...member, ...editData });
      setEditing(false);
      toast.success('Member updated successfully');
    } catch (error) {
      toast.error('Failed to update member');
    }
  };

  const handleCancel = () => {
    setEditData(member || {});
    setEditing(false);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  if (!member) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 text-lg">Member not found</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <button
            onClick={() => navigate('/members')}
            className="mr-4 p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <ArrowLeft className="h-5 w-5" />
          </button>
          <h1 className="text-2xl font-bold text-gray-900">Member Profile</h1>
        </div>
        
        <div className="flex space-x-3">
          {editing ? (
            <>
              <button
                onClick={handleCancel}
                className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <X className="h-4 w-4 mr-2 inline" />
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                <Save className="h-4 w-4 mr-2 inline" />
                Save Changes
              </button>
            </>
          ) : (
            <button
              onClick={() => setEditing(true)}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <Edit className="h-4 w-4 mr-2 inline" />
              Edit Profile
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Card */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="text-center">
              <div className="relative inline-block">
                <div className="w-24 h-24 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mb-4">
                  {member.full_name.charAt(0).toUpperCase()}
                </div>
                {editing && (
                  <button className="absolute bottom-0 right-0 bg-white rounded-full p-2 shadow-lg border border-gray-200 hover:bg-gray-50 transition-colors">
                    <Camera className="h-4 w-4 text-gray-600" />
                  </button>
                )}
              </div>
              
              {editing ? (
                <input
                  type="text"
                  value={editData.full_name || ''}
                  onChange={(e) => setEditData(prev => ({ ...prev, full_name: e.target.value }))}
                  className="text-xl font-bold text-gray-900 text-center border-b border-gray-300 focus:border-primary-500 focus:outline-none bg-transparent"
                />
              ) : (
                <h2 className="text-xl font-bold text-gray-900">{member.full_name}</h2>
              )}
              
              <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium mt-2 ${
                member.is_active 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                {member.is_active ? 'Active Member' : 'Inactive'}
              </div>
            </div>

            <div className="mt-6 space-y-4">
              <div className="flex items-center">
                <Mail className="h-5 w-5 text-gray-400 mr-3" />
                {editing ? (
                  <input
                    type="email"
                    value={editData.email || ''}
                    onChange={(e) => setEditData(prev => ({ ...prev, email: e.target.value }))}
                    className="flex-1 border-b border-gray-300 focus:border-primary-500 focus:outline-none bg-transparent"
                  />
                ) : (
                  <span className="text-gray-600">{member.email}</span>
                )}
              </div>

              <div className="flex items-center">
                <Phone className="h-5 w-5 text-gray-400 mr-3" />
                {editing ? (
                  <input
                    type="tel"
                    value={editData.phone || ''}
                    onChange={(e) => setEditData(prev => ({ ...prev, phone: e.target.value }))}
                    className="flex-1 border-b border-gray-300 focus:border-primary-500 focus:outline-none bg-transparent"
                    placeholder="Phone number"
                  />
                ) : (
                  <span className="text-gray-600">{member.phone || 'Not provided'}</span>
                )}
              </div>

              <div className="flex items-center">
                <Calendar className="h-5 w-5 text-gray-400 mr-3" />
                <span className="text-gray-600">
                  Joined {format(new Date(member.created_at || ''), 'MMM dd, yyyy')}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* Subscription Info */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <CreditCard className="h-5 w-5 mr-2" />
              Subscription Details
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Due Date
                </label>
                {editing ? (
                  <input
                    type="date"
                    value={editData.subscription_due_date || ''}
                    onChange={(e) => setEditData(prev => ({ ...prev, subscription_due_date: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                ) : (
                  <div className="text-gray-900 font-medium">
                    {format(new Date(member.subscription_due_date), 'MMM dd, yyyy')}
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Status
                </label>
                {editing ? (
                  <select
                    value={editData.is_active ? 'active' : 'inactive'}
                    onChange={(e) => setEditData(prev => ({ ...prev, is_active: e.target.value === 'active' }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                  </select>
                ) : (
                  <div className={`font-medium ${member.is_active ? 'text-green-600' : 'text-red-600'}`}>
                    {member.is_active ? 'Active' : 'Inactive'}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Personal Info */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              Personal Information
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Birthday
                </label>
                {editing ? (
                  <input
                    type="date"
                    value={editData.birthday || ''}
                    onChange={(e) => setEditData(prev => ({ ...prev, birthday: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                ) : (
                  <div className="text-gray-900">
                    {member.birthday ? format(new Date(member.birthday), 'MMM dd, yyyy') : 'Not provided'}
                  </div>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Last Check-in
                </label>
                {editing ? (
                  <input
                    type="date"
                    value={editData.last_checkin_date || ''}
                    onChange={(e) => setEditData(prev => ({ ...prev, last_checkin_date: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                ) : (
                  <div className="text-gray-900">
                    {member.last_checkin_date ? format(new Date(member.last_checkin_date), 'MMM dd, yyyy') : 'Never'}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Milestones */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Trophy className="h-5 w-5 mr-2" />
              Achievements & Milestones
            </h3>
            
            {editing ? (
              <div className="space-y-3">
                {(editData.milestones || []).map((milestone, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <input
                      type="text"
                      value={milestone}
                      onChange={(e) => {
                        const newMilestones = [...(editData.milestones || [])];
                        newMilestones[index] = e.target.value;
                        setEditData(prev => ({ ...prev, milestones: newMilestones }));
                      }}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    />
                    <button
                      onClick={() => {
                        const newMilestones = (editData.milestones || []).filter((_, i) => i !== index);
                        setEditData(prev => ({ ...prev, milestones: newMilestones }));
                      }}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                ))}
                <button
                  onClick={() => {
                    const newMilestones = [...(editData.milestones || []), ''];
                    setEditData(prev => ({ ...prev, milestones: newMilestones }));
                  }}
                  className="w-full px-3 py-2 border-2 border-dashed border-gray-300 rounded-lg text-gray-500 hover:border-primary-300 hover:text-primary-600 transition-colors"
                >
                  Add Milestone
                </button>
              </div>
            ) : (
              <div className="space-y-2">
                {member.milestones && member.milestones.length > 0 ? (
                  member.milestones.map((milestone, index) => (
                    <div key={index} className="flex items-center p-3 bg-accent-50 rounded-lg">
                      <Trophy className="h-4 w-4 text-accent-600 mr-3" />
                      <span className="text-gray-900">{milestone}</span>
                    </div>
                  ))
                ) : (
                  <div className="text-gray-500 text-center py-4">
                    No milestones recorded yet
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};