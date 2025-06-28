import React, { useState, useEffect } from 'react';
import { 
  Calendar, 
  Activity, 
  TrendingUp, 
  Clock, 
  Target,
  Award,
  Users,
  CheckCircle,
  XCircle,
  Upload
} from 'lucide-react';
import { apiService } from '../../services/apiService';
import { format } from 'date-fns';
import toast from 'react-hot-toast';

interface MemberPortalData {
  member: any;
  current_workout_plan: any;
  recent_workouts: any[];
  upcoming_sessions: any[];
  stats: {
    total_workouts: number;
    this_month_workouts: number;
    workout_streak: number;
    membership_status: string;
    days_until_due: number;
  };
}

export const MemberPortal: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<MemberPortalData | null>(null);
  const [loading, setLoading] = useState(true);
  const [checkedIn, setCheckedIn] = useState(false);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await apiService.getMemberPortalDashboard();
      setDashboardData(data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
      toast.error('Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleCheckin = async () => {
    try {
      if (checkedIn) {
        await apiService.checkout();
        toast.success('Checked out successfully!');
        setCheckedIn(false);
      } else {
        await apiService.checkin();
        toast.success('Checked in successfully!');
        setCheckedIn(true);
      }
    } catch (error: any) {
      toast.error(error.message || 'Check-in failed');
    }
  };

  const StatCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ElementType;
    color: string;
  }> = ({ title, value, icon: Icon, color }) => (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
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

  if (!dashboardData) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 text-lg">Unable to load dashboard</div>
      </div>
    );
  }

  const { member, current_workout_plan, recent_workouts, upcoming_sessions, stats } = dashboardData;

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Welcome back, {member.full_name}!</h1>
            <p className="text-gray-600 mt-1">Track your fitness journey and stay motivated</p>
          </div>
          
          <button
            onClick={handleCheckin}
            className={`px-6 py-3 rounded-lg font-medium transition-colors ${
              checkedIn
                ? 'bg-red-600 text-white hover:bg-red-700'
                : 'bg-green-600 text-white hover:bg-green-700'
            }`}
          >
            {checkedIn ? 'Check Out' : 'Check In'}
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Workouts"
          value={stats.total_workouts}
          icon={Activity}
          color="bg-blue-500"
        />
        <StatCard
          title="This Month"
          value={stats.this_month_workouts}
          icon={Calendar}
          color="bg-green-500"
        />
        <StatCard
          title="Workout Streak"
          value={`${stats.workout_streak} days`}
          icon={TrendingUp}
          color="bg-purple-500"
        />
        <StatCard
          title="Membership"
          value={stats.membership_status}
          icon={Award}
          color="bg-orange-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Current Workout Plan */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Target className="h-5 w-5 mr-2" />
            Current Workout Plan
          </h3>
          
          {current_workout_plan ? (
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-gray-900">{current_workout_plan.workout_plan.name}</h4>
                <p className="text-sm text-gray-600">{current_workout_plan.workout_plan.description}</p>
              </div>
              
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Difficulty:</span>
                  <span className="ml-2 font-medium capitalize">{current_workout_plan.workout_plan.difficulty_level}</span>
                </div>
                <div>
                  <span className="text-gray-500">Duration:</span>
                  <span className="ml-2 font-medium">{current_workout_plan.workout_plan.duration_weeks} weeks</span>
                </div>
              </div>
              
              {current_workout_plan.coach && (
                <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <span className="text-sm font-medium text-primary-800">
                      {current_workout_plan.coach.full_name.charAt(0)}
                    </span>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{current_workout_plan.coach.full_name}</p>
                    <p className="text-xs text-gray-500">Your Coach</p>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-8">
              <Target className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No active workout plan</p>
              <p className="text-sm text-gray-400 mt-1">Contact your coach to get started</p>
            </div>
          )}
        </div>

        {/* Recent Workouts */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Activity className="h-5 w-5 mr-2" />
            Recent Workouts
          </h3>
          
          {recent_workouts.length > 0 ? (
            <div className="space-y-3">
              {recent_workouts.slice(0, 5).map((workout) => (
                <div key={workout.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    {workout.completed ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : (
                      <XCircle className="h-5 w-5 text-red-500" />
                    )}
                    <div>
                      <p className="text-sm font-medium text-gray-900">{workout.workout_session.name}</p>
                      <p className="text-xs text-gray-500">{format(new Date(workout.date), 'MMM dd, yyyy')}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">{workout.duration_minutes}m</p>
                    {workout.rating && (
                      <div className="flex items-center">
                        {[...Array(5)].map((_, i) => (
                          <span
                            key={i}
                            className={`text-xs ${i < workout.rating ? 'text-yellow-400' : 'text-gray-300'}`}
                          >
                            ★
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Activity className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No workouts logged yet</p>
              <p className="text-sm text-gray-400 mt-1">Start your fitness journey today!</p>
            </div>
          )}
        </div>

        {/* Upcoming Sessions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Clock className="h-5 w-5 mr-2" />
            Upcoming Sessions
          </h3>
          
          {upcoming_sessions.length > 0 ? (
            <div className="space-y-3">
              {upcoming_sessions.map((session) => (
                <div key={session.id} className="p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900">{session.title}</p>
                      <p className="text-sm text-gray-600">{session.session_type}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">
                        {format(new Date(session.date), 'MMM dd')}
                      </p>
                      <p className="text-sm text-gray-500">
                        {session.start_time} - {session.end_time}
                      </p>
                    </div>
                  </div>
                  
                  {session.coach && (
                    <div className="mt-2 flex items-center space-x-2">
                      <Users className="h-4 w-4 text-gray-400" />
                      <span className="text-sm text-gray-600">{session.coach.full_name}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Clock className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">No upcoming sessions</p>
              <p className="text-sm text-gray-400 mt-1">Book a session with a trainer</p>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          
          <div className="space-y-3">
            <button className="w-full flex items-center justify-between p-3 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors">
              <div className="flex items-center">
                <Activity className="h-5 w-5 text-primary-600 mr-3" />
                <span className="text-primary-900 font-medium">Log Workout</span>
              </div>
              <span className="text-primary-600">→</span>
            </button>
            
            <button className="w-full flex items-center justify-between p-3 bg-green-50 rounded-lg hover:bg-green-100 transition-colors">
              <div className="flex items-center">
                <Users className="h-5 w-5 text-green-600 mr-3" />
                <span className="text-green-900 font-medium">Book Session</span>
              </div>
              <span className="text-green-600">→</span>
            </button>
            
            <button className="w-full flex items-center justify-between p-3 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
              <div className="flex items-center">
                <Target className="h-5 w-5 text-purple-600 mr-3" />
                <span className="text-purple-900 font-medium">View Plans</span>
              </div>
              <span className="text-purple-600">→</span>
            </button>
            
            <button className="w-full flex items-center justify-between p-3 bg-orange-50 rounded-lg hover:bg-orange-100 transition-colors">
              <div className="flex items-center">
                <Upload className="h-5 w-5 text-orange-600 mr-3" />
                <span className="text-orange-900 font-medium">Update Profile</span>
              </div>
              <span className="text-orange-600">→</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};