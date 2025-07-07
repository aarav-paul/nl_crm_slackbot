import { useState } from 'react'
import { 
  CogIcon, 
  KeyIcon, 
  UserIcon,
  BellIcon,
  ShieldCheckIcon,
  CloudIcon
} from '@heroicons/react/24/outline'

export default function Settings() {
  const [activeTab, setActiveTab] = useState('general')

  const tabs = [
    { id: 'general', name: 'General', icon: CogIcon },
    { id: 'salesforce', name: 'Salesforce', icon: CloudIcon },
    { id: 'ai', name: 'AI Settings', icon: ShieldCheckIcon },
    { id: 'notifications', name: 'Notifications', icon: BellIcon },
    { id: 'account', name: 'Account', icon: UserIcon },
  ]

  const renderTabContent = () => {
    switch (activeTab) {
      case 'general':
        return <GeneralSettings />
      case 'salesforce':
        return <SalesforceSettings />
      case 'ai':
        return <AISettings />
      case 'notifications':
        return <NotificationSettings />
      case 'account':
        return <AccountSettings />
      default:
        return <GeneralSettings />
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Settings Navigation */}
        <div className="lg:col-span-1">
          <nav className="space-y-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                  activeTab === tab.id
                    ? 'bg-slate-900 text-white'
                    : 'text-slate-700 hover:bg-slate-100'
                }`}
              >
                <tab.icon className="h-5 w-5 mr-3" />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        {/* Settings Content */}
        <div className="lg:col-span-3">
          {renderTabContent()}
        </div>
      </div>
    </div>
  )
}

function GeneralSettings() {
  return (
    <div className="card">
      <div className="p-6 border-b border-slate-200">
        <h3 className="text-lg font-medium text-slate-900">General Settings</h3>
        <p className="text-sm text-slate-500 mt-1">Manage your application preferences</p>
      </div>
      <div className="p-6 space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Application Name
          </label>
          <input
            type="text"
            defaultValue="Salesforce AI Dashboard"
            className="input"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Time Zone
          </label>
          <select className="input">
            <option>UTC-8 (Pacific Time)</option>
            <option>UTC-5 (Eastern Time)</option>
            <option>UTC+0 (GMT)</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Date Format
          </label>
          <select className="input">
            <option>MM/DD/YYYY</option>
            <option>DD/MM/YYYY</option>
            <option>YYYY-MM-DD</option>
          </select>
        </div>

        <div className="pt-4">
          <button className="btn btn-primary">Save Changes</button>
        </div>
      </div>
    </div>
  )
}

function SalesforceSettings() {
  return (
    <div className="space-y-6">
      <div className="card">
        <div className="p-6 border-b border-slate-200">
          <h3 className="text-lg font-medium text-slate-900">Salesforce Connection</h3>
          <p className="text-sm text-slate-500 mt-1">Manage your Salesforce integration</p>
        </div>
        <div className="p-6">
          <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="h-3 w-3 bg-green-500 rounded-full"></div>
              <div>
                <p className="text-sm font-medium text-green-800">Connected to Salesforce</p>
                <p className="text-sm text-green-600">Last sync: 2 minutes ago</p>
              </div>
            </div>
            <button className="btn btn-secondary text-sm">
              Reconnect
            </button>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="p-6 border-b border-slate-200">
          <h3 className="text-lg font-medium text-slate-900">API Configuration</h3>
        </div>
        <div className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Salesforce Instance URL
            </label>
            <input
              type="text"
              defaultValue="https://yourorg.salesforce.com"
              className="input"
              disabled
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              API Version
            </label>
            <select className="input">
              <option>v59.0</option>
              <option>v58.0</option>
              <option>v57.0</option>
            </select>
          </div>

          <div className="pt-4">
            <button className="btn btn-primary">Update Configuration</button>
          </div>
        </div>
      </div>
    </div>
  )
}

function AISettings() {
  return (
    <div className="card">
      <div className="p-6 border-b border-slate-200">
        <h3 className="text-lg font-medium text-slate-900">AI Assistant Settings</h3>
        <p className="text-sm text-slate-500 mt-1">Configure AI processing preferences</p>
      </div>
      <div className="p-6 space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            AI Model
          </label>
          <select className="input">
            <option>GPT-4o (Recommended)</option>
            <option>GPT-4o-mini</option>
            <option>GPT-4</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Response Confidence Threshold
          </label>
          <input
            type="range"
            min="0"
            max="100"
            defaultValue="85"
            className="w-full"
          />
          <div className="flex justify-between text-sm text-slate-500 mt-1">
            <span>Low (0%)</span>
            <span>High (100%)</span>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div>
            <h4 className="text-sm font-medium text-slate-900">Auto-execute simple commands</h4>
            <p className="text-sm text-slate-500">Skip confirmation for basic operations</p>
          </div>
          <input type="checkbox" className="h-4 w-4 text-slate-600" />
        </div>

        <div className="pt-4">
          <button className="btn btn-primary">Save AI Settings</button>
        </div>
      </div>
    </div>
  )
}

function NotificationSettings() {
  return (
    <div className="card">
      <div className="p-6 border-b border-slate-200">
        <h3 className="text-lg font-medium text-slate-900">Notification Preferences</h3>
        <p className="text-sm text-slate-500 mt-1">Choose what notifications you want to receive</p>
      </div>
      <div className="p-6 space-y-6">
        {[
          { title: 'Lead Updates', desc: 'When lead status changes' },
          { title: 'AI Command Results', desc: 'Success/failure notifications' },
          { title: 'System Alerts', desc: 'Important system messages' },
          { title: 'Weekly Reports', desc: 'Summary of lead activity' },
        ].map((item, index) => (
          <div key={index} className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-medium text-slate-900">{item.title}</h4>
              <p className="text-sm text-slate-500">{item.desc}</p>
            </div>
            <input type="checkbox" defaultChecked className="h-4 w-4 text-slate-600" />
          </div>
        ))}

        <div className="pt-4">
          <button className="btn btn-primary">Save Preferences</button>
        </div>
      </div>
    </div>
  )
}

function AccountSettings() {
  return (
    <div className="card">
      <div className="p-6 border-b border-slate-200">
        <h3 className="text-lg font-medium text-slate-900">Account Information</h3>
        <p className="text-sm text-slate-500 mt-1">Manage your account details</p>
      </div>
      <div className="p-6 space-y-6">
        <div className="flex items-center space-x-4">
          <div className="h-16 w-16 rounded-full bg-slate-200 flex items-center justify-center">
            <UserIcon className="h-8 w-8 text-slate-500" />
          </div>
          <div>
            <h4 className="text-lg font-medium text-slate-900">Project Manager</h4>
            <p className="text-sm text-slate-500">project.manager@company.com</p>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Full Name
          </label>
          <input
            type="text"
            defaultValue="Project Manager"
            className="input"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Email Address
          </label>
          <input
            type="email"
            defaultValue="project.manager@company.com"
            className="input"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Role
          </label>
          <select className="input">
            <option>Project Manager</option>
            <option>Sales Manager</option>
            <option>Administrator</option>
          </select>
        </div>

        <div className="pt-4 space-x-3">
          <button className="btn btn-primary">Update Account</button>
          <button className="btn btn-secondary">Change Password</button>
        </div>
      </div>
    </div>
  )
}