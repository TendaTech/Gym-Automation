import React from 'react';
import { Dumbbell, Users, Mail, Calendar } from 'lucide-react';

interface HeaderProps {
  memberCount: number;
  dueSoonCount: number;
  onSendReminders: () => void;
  isLoading?: boolean;
}

export const Header: React.FC<HeaderProps> = ({ 
  memberCount, 
  dueSoonCount, 
  onSendReminders, 
  isLoading 
}) => {
  return (
    <div className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          <div className="flex items-center">
            <div className="flex items-center">
              <Dumbbell className="h-8 w-8 text-primary-500" />
              <h1 className="ml-3 text-2xl font-bold text-gray-900">
                Gym Automation System
              </h1>
            </div>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm">
                <Users className="h-4 w-4 text-gray-500" />
                <span className="text-gray-600">{memberCount} Members</span>
              </div>
              
              <div className="flex items-center space-x-2 text-sm">
                <Calendar className="h-4 w-4 text-orange-500" />
                <span className="text-orange-600">{dueSoonCount} Due Soon</span>
              </div>
            </div>
            
            <button
              onClick={onSendReminders}
              disabled={isLoading}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Mail className="h-4 w-4 mr-2" />
              {isLoading ? 'Sending...' : 'Send Reminders'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};