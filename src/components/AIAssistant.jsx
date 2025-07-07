import { useState } from 'react'
import { 
  SparklesIcon, 
  PaperAirplaneIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationCircleIcon
} from '@heroicons/react/24/outline'

const exampleCommands = [
  "Create a new lead for Jane Smith with email jane@company.com",
  "Update John Doe's lead status to Qualified",
  "Delete the lead for Mike Johnson",
  "Show me all leads with status Working",
  "Create a lead for Sarah Wilson at TechCorp with phone 555-0123"
]

const mockHistory = [
  {
    id: 1,
    command: "Create a new lead for Jane Smith with email jane@company.com",
    status: 'completed',
    timestamp: '2024-01-16T10:30:00Z',
    result: 'Successfully created lead "Jane Smith" with ID: 003XX000004TmiQ'
  },
  {
    id: 2,
    command: "Update John Doe's lead status to Qualified",
    status: 'completed',
    timestamp: '2024-01-16T09:15:00Z',
    result: 'Successfully updated John Doe to status "Qualified"'
  },
  {
    id: 3,
    command: "Delete the lead for Mike Johnson",
    status: 'failed',
    timestamp: '2024-01-16T08:45:00Z',
    result: 'Error: Lead "Mike Johnson" not found in Salesforce'
  },
]

export default function AIAssistant() {
  const [command, setCommand] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [pendingCommand, setPendingCommand] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!command.trim()) return

    setIsProcessing(true)
    
    // Simulate AI processing
    setTimeout(() => {
      setPendingCommand({
        id: Date.now(),
        command: command,
        parsedAction: {
          tool: 'salesforce',
          action: 'create',
          object: 'Lead',
          fields: {
            Name: 'Jane Smith',
            Email: 'jane@company.com',
            Company: 'Smith Corp'
          }
        }
      })
      setIsProcessing(false)
      setCommand('')
    }, 2000)
  }

  const executeCommand = () => {
    // Simulate execution
    setTimeout(() => {
      setPendingCommand(null)
      // Add to history in real implementation
    }, 1500)
  }

  const cancelCommand = () => {
    setPendingCommand(null)
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />
      case 'failed':
        return <ExclamationCircleIcon className="h-5 w-5 text-red-500" />
      case 'processing':
        return <ClockIcon className="h-5 w-5 text-yellow-500" />
      default:
        return <ClockIcon className="h-5 w-5 text-slate-400" />
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* AI Command Interface */}
      <div className="card">
        <div className="p-6 border-b border-slate-200">
          <div className="flex items-center space-x-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-900">
              <SparklesIcon className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-slate-900">AI Assistant</h2>
              <p className="text-sm text-slate-500">Use natural language to manage your Salesforce leads</p>
            </div>
          </div>
        </div>

        <div className="p-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="command" className="block text-sm font-medium text-slate-700 mb-2">
                Enter your command
              </label>
              <div className="relative">
                <textarea
                  id="command"
                  rows={3}
                  value={command}
                  onChange={(e) => setCommand(e.target.value)}
                  placeholder="e.g., Create a new lead for John Smith with email john@company.com"
                  className="input resize-none"
                  disabled={isProcessing}
                />
                <button
                  type="submit"
                  disabled={!command.trim() || isProcessing}
                  className="absolute bottom-3 right-3 btn btn-primary p-2 disabled:opacity-50"
                >
                  {isProcessing ? (
                    <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
                  ) : (
                    <PaperAirplaneIcon className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>

            {/* Example Commands */}
            <div>
              <p className="text-sm font-medium text-slate-700 mb-2">Example commands:</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {exampleCommands.map((example, index) => (
                  <button
                    key={index}
                    type="button"
                    onClick={() => setCommand(example)}
                    className="text-left p-3 text-sm bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors"
                    disabled={isProcessing}
                  >
                    "{example}"
                  </button>
                ))}
              </div>
            </div>
          </form>
        </div>
      </div>

      {/* Pending Command Confirmation */}
      {pendingCommand && (
        <div className="card border-blue-200 bg-blue-50">
          <div className="p-6">
            <h3 className="text-lg font-medium text-slate-900 mb-4">Command Parsed Successfully</h3>
            
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-slate-700">Original Command:</p>
                <p className="text-sm text-slate-600 bg-white p-3 rounded-lg mt-1">
                  {pendingCommand.command}
                </p>
              </div>

              <div>
                <p className="text-sm font-medium text-slate-700">Parsed Action:</p>
                <div className="bg-white p-3 rounded-lg mt-1 text-sm">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="font-medium">Action:</span> {pendingCommand.parsedAction.action}
                    </div>
                    <div>
                      <span className="font-medium">Object:</span> {pendingCommand.parsedAction.object}
                    </div>
                  </div>
                  {pendingCommand.parsedAction.fields && (
                    <div className="mt-2">
                      <span className="font-medium">Fields:</span>
                      <ul className="mt-1 space-y-1">
                        {Object.entries(pendingCommand.parsedAction.fields).map(([key, value]) => (
                          <li key={key} className="text-slate-600">
                            • {key}: {value}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>

              <div className="flex space-x-3 pt-4">
                <button
                  onClick={executeCommand}
                  className="btn btn-primary"
                >
                  Execute Command
                </button>
                <button
                  onClick={cancelCommand}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Command History */}
      <div className="card">
        <div className="p-6 border-b border-slate-200">
          <h3 className="text-lg font-medium text-slate-900">Recent Commands</h3>
        </div>
        <div className="divide-y divide-slate-200">
          {mockHistory.map((item) => (
            <div key={item.id} className="p-6">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 mt-1">
                  {getStatusIcon(item.status)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-slate-900">
                      {item.command}
                    </p>
                    <p className="text-sm text-slate-500">
                      {new Date(item.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <p className={`mt-1 text-sm ${
                    item.status === 'completed' ? 'text-green-600' : 
                    item.status === 'failed' ? 'text-red-600' : 'text-slate-600'
                  }`}>
                    {item.result}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}