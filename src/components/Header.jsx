import { Bars3Icon, BellIcon } from '@heroicons/react/24/outline'

const viewTitles = {
  dashboard: 'Dashboard',
  leads: 'Lead Management',
  'ai-assistant': 'AI Assistant',
  analytics: 'Analytics',
  settings: 'Settings'
}

export default function Header({ setSidebarOpen, currentView }) {
  return (
    <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-slate-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
      <button
        type="button"
        className="-m-2.5 p-2.5 text-slate-700 lg:hidden"
        onClick={() => setSidebarOpen(true)}
      >
        <Bars3Icon className="h-6 w-6" />
      </button>

      {/* Separator */}
      <div className="h-6 w-px bg-slate-200 lg:hidden" />

      <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
        <div className="flex items-center">
          <h1 className="text-xl font-semibold text-slate-900">
            {viewTitles[currentView] || 'Dashboard'}
          </h1>
        </div>
        
        <div className="flex flex-1 justify-end items-center gap-x-4 lg:gap-x-6">
          {/* Search */}
          <div className="hidden sm:block">
            <div className="relative">
              <input
                type="text"
                placeholder="Search leads..."
                className="input w-64"
              />
            </div>
          </div>

          {/* Notifications */}
          <button
            type="button"
            className="-m-2.5 p-2.5 text-slate-400 hover:text-slate-500"
          >
            <BellIcon className="h-6 w-6" />
          </button>

          {/* Connection status */}
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 rounded-full bg-green-500"></div>
            <span className="text-sm text-slate-600">Connected</span>
          </div>
        </div>
      </div>
    </div>
  )
}