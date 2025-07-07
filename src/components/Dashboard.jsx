import React from 'react'
import { 
  UsersIcon, 
  ArrowTrendingUpIcon, 
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'

const stats = [
  {
    name: 'Total Leads',
    value: '2,847',
    change: '+12%',
    changeType: 'increase',
    icon: UsersIcon,
  },
  {
    name: 'Qualified Leads',
    value: '1,234',
    change: '+8%',
    changeType: 'increase',
    icon: CheckCircleIcon,
  },
  {
    name: 'Conversion Rate',
    value: '43.2%',
    change: '+2.1%',
    changeType: 'increase',
    icon: ArrowTrendingUpIcon,
  },
  {
    name: 'Pending Actions',
    value: '23',
    change: '-5',
    changeType: 'decrease',
    icon: ClockIcon,
  },
]

const recentActivity = [
  {
    id: 1,
    type: 'lead_created',
    message: 'New lead "Sarah Johnson" created via AI Assistant',
    time: '2 minutes ago',
    icon: UsersIcon,
    iconColor: 'text-green-600',
    bgColor: 'bg-green-50',
  },
  {
    id: 2,
    type: 'status_updated',
    message: 'Lead "John Doe" status updated to Qualified',
    time: '15 minutes ago',
    icon: CheckCircleIcon,
    iconColor: 'text-blue-600',
    bgColor: 'bg-blue-50',
  },
  {
    id: 3,
    type: 'lead_deleted',
    message: 'Lead "Mike Wilson" removed from system',
    time: '1 hour ago',
    icon: ExclamationTriangleIcon,
    iconColor: 'text-red-600',
    bgColor: 'bg-red-50',
  },
  {
    id: 4,
    type: 'ai_command',
    message: 'AI processed 12 commands successfully today',
    time: '2 hours ago',
    icon: ArrowTrendingUpIcon,
    iconColor: 'text-purple-600',
    bgColor: 'bg-purple-50',
  },
]

export default function Dashboard() {
  return (
    <div className="space-y-8">
      {/* Stats */}
      <div>
        <h2 className="text-lg font-medium text-slate-900 mb-4">Overview</h2>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <div key={stat.name} className="card p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <stat.icon className="h-8 w-8 text-slate-600" />
                </div>
                <div className="ml-4 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-slate-500 truncate">
                      {stat.name}
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-slate-900">
                        {stat.value}
                      </div>
                      <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                        stat.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {stat.change}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Activity */}
        <div className="card">
          <div className="p-6 border-b border-slate-200">
            <h3 className="text-lg font-medium text-slate-900">Recent Activity</h3>
          </div>
          <div className="p-6">
            <div className="flow-root">
              <ul className="-mb-8">
                {recentActivity.map((activity, activityIdx) => (
                  <li key={activity.id}>
                    <div className="relative pb-8">
                      {activityIdx !== recentActivity.length - 1 ? (
                        <span
                          className="absolute left-4 top-4 -ml-px h-full w-0.5 bg-slate-200"
                          aria-hidden="true"
                        />
                      ) : null}
                      <div className="relative flex space-x-3">
                        <div>
                          <span className={`${activity.bgColor} h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white`}>
                            <activity.icon className={`h-4 w-4 ${activity.iconColor}`} />
                          </span>
                        </div>
                        <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                          <div>
                            <p className="text-sm text-slate-900">{activity.message}</p>
                          </div>
                          <div className="whitespace-nowrap text-right text-sm text-slate-500">
                            {activity.time}
                          </div>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <div className="p-6 border-b border-slate-200">
            <h3 className="text-lg font-medium text-slate-900">Quick Actions</h3>
          </div>
          <div className="p-6 space-y-4">
            <button className="btn btn-primary w-full justify-start">
              <UsersIcon className="h-5 w-5 mr-2" />
              Create New Lead
            </button>
            <button className="btn btn-secondary w-full justify-start">
              <ArrowTrendingUpIcon className="h-5 w-5 mr-2" />
              Bulk Update Status
            </button>
            <button className="btn btn-secondary w-full justify-start">
              <ClockIcon className="h-5 w-5 mr-2" />
              Review Pending Leads
            </button>
            
            <div className="pt-4 border-t border-slate-200">
              <h4 className="text-sm font-medium text-slate-900 mb-3">AI Assistant</h4>
              <div className="space-y-2">
                <div className="p-3 bg-slate-50 rounded-lg">
                  <p className="text-sm text-slate-700">Try: "Create a lead for Jane Smith with email jane@company.com"</p>
                </div>
                <div className="p-3 bg-slate-50 rounded-lg">
                  <p className="text-sm text-slate-700">Try: "Update John Doe's status to Qualified"</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}