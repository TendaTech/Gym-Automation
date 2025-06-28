import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Calendar, 
  TrendingUp, 
  DollarSign, 
  Activity,
  Clock,
  UserCheck,
  AlertTriangle,
  Cake
} from 'lucide-react';
import { MemberService } from '../../services/memberService';
import { Member } from '../../types/member';
import { format, startOfMonth, endOfMonth, isWithinInterval } from 'date-fns';

export const DashboardHome: React.FC = () => {
  const [stats, setStats] = useState({
    totalMembers: 0,
    activeMembers: 0,
    dueSoon: 0,
    revenue: 0,
    newThisMonth: 0,
    birthdaysToday: 0
  });
  const [recentMembers, setRecentMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const allMembers = await MemberService.getAllMembers();
      const dueSoonMembers = await MemberService.getFilteredMembers('due_soon');
      const birthdayMembers = await MemberService.getFilteredMembers('birthdays');
      
      const now = new Date();
      const monthStart = startOfMonth(now);
      const monthEnd = endOfMonth(now);
      
      const newThisMonth = allMembers.filter(member => 
        member.created_at && isWithinInterval(new Date(member.created_at), { start: monthStart, end: monthEnd })
      ).length;

      setStats({
        totalMembers: allMembers.length,
        activeMembers: allMembers.filter(m => m.is_active).length,
        dueSoon: dueSoonMembers.length,
        revenue: allMembers.filter(m => m.is_active).length * 50, // Assuming $50 per member
        newThisMonth,
        birthdaysToday: birthdayMembers.length
      });

      // Get 5 most recent members
      const recent = allMembers
        .sort((a, b) => new Date(b.created_at || '').getTime() - new Date(a.created_at || '').getTime())
        .slice(0, 5);
      setRecentMembers(recent);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ElementType;
    color: string;
    trend?: string;
  }> = ({ title, value, icon: Icon, color, trend }) => (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {trend && (
            <p className="text-sm text-green-600 mt-1 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              {trend}
            </p>
          )}
        </div>
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Welcome back! Here's what's happening at your gym.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6 mb-8">
        <StatCard
          title="Total Members"
          value={stats.totalMembers}
          icon={Users}
          color="bg-blue-500"
          trend="+12% from last month"
        />
        <StatCard
          title="Active Members"
          value={stats.activeMembers}
          icon={UserCheck}
          color="bg-green-500"
        />
        <StatCard
          title="Due Soon"
          value={stats.dueSoon}
          icon={Clock}
          color="bg-yellow-500"
        />
        <StatCard
          title="Monthly Revenue"
          value={`$${stats.revenue.toLocaleString()}`}
          icon={DollarSign}
          color="bg-purple-500"
          trend="+8% from last month"
        />
        <StatCard
          title="New This Month"
          value={stats.newThisMonth}
          icon={TrendingUp}
          color="bg-indigo-500"
        />
        <StatCard
          title="Birthdays Today"
          value={stats.birthdaysToday}
          icon={Cake}
          color="bg-pink-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Members */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Members</h3>
          <div className="space-y-4">
            {recentMembers.map((member) => (
              <div key={member.id} className="flex items-center space-x-4">
                <div className="flex-shrink-0">
                  <div className="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                    <span className="text-sm font-medium text-primary-800">
                      {member.full_name.charAt(0).toUpperCase()}
                    </span>
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {member.full_name}
                  </p>
                  <p className="text-sm text-gray-500 truncate">
                    {member.email}
                  </p>
                </div>
                <div className="text-sm text-gray-500">
                  {member.created_at && format(new Date(member.created_at), 'MMM dd')}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button className="w-full flex items-center justify-between p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors">
              <div className="flex items-center">
                <Users className="h-5 w-5 text-primary-600 mr-3" />
                <span className="text-primary-900 font-medium">Add New Member</span>
              </div>
              <span className="text-primary-600">→</span>
            </button>
            
            <button className="w-full flex items-center justify-between p-4 bg-yellow-50 rounded-lg hover:bg-yellow-100 transition-colors">
              <div className="flex items-center">
                <Clock className="h-5 w-5 text-yellow-600 mr-3" />
                <span className="text-yellow-900 font-medium">Send Reminders</span>
              </div>
              <span className="text-yellow-600">→</span>
            </button>
            
            <button className="w-full flex items-center justify-between p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <div className="flex items-center">
                <Activity className="h-5 w-5 text-green-600 mr-3" />
                <span className="text-green-900 font-medium">View Reports</span>
              </div>
              <span className="text-green-600">→</span>
            </button>
            
            <button className="w-full flex items-center justify-between p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <div className="flex items-center">
                <Calendar className="h-5 w-5 text-purple-600 mr-3" />
                <span className="text-purple-900 font-medium">Manage Schedule</span>
              </div>
              <span className="text-purple-600">→</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};