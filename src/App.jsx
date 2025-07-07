import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './components/Dashboard'
import LeadsView from './components/LeadsView'
import AIAssistant from './components/AIAssistant'
import Settings from './components/Settings'

function App() {
  const [currentView, setCurrentView] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const renderCurrentView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard />
      case 'leads':
        return <LeadsView />
      case 'ai-assistant':
        return <AIAssistant />
      case 'settings':
        return <Settings />
      default:
        return <Dashboard />
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar 
        currentView={currentView}
        setCurrentView={setCurrentView}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
      />
      
      <div className="lg:pl-72">
        <Header 
          setSidebarOpen={setSidebarOpen}
          currentView={currentView}
        />
        
        <main className="py-8">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            {renderCurrentView()}
          </div>
        </main>
      </div>
    </div>
  )
}

export default App