import React from 'react';
import { FilterType } from '../types/member';
import { Users, Clock, UserX, Cake, CheckCircle } from 'lucide-react';

interface FilterTabsProps {
  activeFilter: FilterType;
  onFilterChange: (filter: FilterType) => void;
  counts: {
    all: number;
    due_soon: number;
    inactive: number;
    birthdays: number;
    active_only: number;
  };
}

export const FilterTabs: React.FC<FilterTabsProps> = ({ 
  activeFilter, 
  onFilterChange, 
  counts 
}) => {
  const tabs = [
    { id: 'all' as FilterType, label: 'All Members', icon: Users, count: counts.all },
    { id: 'due_soon' as FilterType, label: 'Due Soon', icon: Clock, count: counts.due_soon },
    { id: 'inactive' as FilterType, label: 'Inactive', icon: UserX, count: counts.inactive },
    { id: 'birthdays' as FilterType, label: 'Birthdays', icon: Cake, count: counts.birthdays },
    { id: 'active_only' as FilterType, label: 'Active Only', icon: CheckCircle, count: counts.active_only },
  ];

  return (
    <div className="border-b border-gray-200 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeFilter === tab.id;
            
            return (
              <button
                key={tab.id}
                onClick={() => onFilterChange(tab.id)}
                className={`
                  group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-colors
                  ${isActive
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon className={`
                  -ml-0.5 mr-2 h-4 w-4 transition-colors
                  ${isActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'}
                `} />
                {tab.label}
                <span className={`
                  ml-2 py-0.5 px-2 rounded-full text-xs font-medium
                  ${isActive 
                    ? 'bg-primary-100 text-primary-600' 
                    : 'bg-gray-100 text-gray-600'
                  }
                `}>
                  {tab.count}
                </span>
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
};