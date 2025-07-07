import { useState } from 'react'
import { 
  PlusIcon, 
  FunnelIcon, 
  MagnifyingGlassIcon,
  EllipsisVerticalIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/react/24/outline'
import { Menu, Transition } from '@headlessui/react'
import { Fragment } from 'react'

const mockLeads = [
  {
    id: '1',
    name: 'Sarah Johnson',
    email: 'sarah.johnson@techcorp.com',
    company: 'TechCorp Solutions',
    status: 'New',
    source: 'Website',
    createdDate: '2024-01-15',
    lastActivity: '2024-01-15',
  },
  {
    id: '2',
    name: 'John Doe',
    email: 'john.doe@innovate.com',
    company: 'Innovate Inc',
    status: 'Qualified',
    source: 'Referral',
    createdDate: '2024-01-14',
    lastActivity: '2024-01-16',
  },
  {
    id: '3',
    name: 'Emily Chen',
    email: 'emily.chen@startup.io',
    company: 'Startup.io',
    status: 'Working',
    source: 'Cold Call',
    createdDate: '2024-01-13',
    lastActivity: '2024-01-16',
  },
  {
    id: '4',
    name: 'Michael Brown',
    email: 'michael@enterprise.com',
    company: 'Enterprise Corp',
    status: 'Nurturing',
    source: 'Trade Show',
    createdDate: '2024-01-12',
    lastActivity: '2024-01-15',
  },
]

const statusColors = {
  'New': 'bg-blue-100 text-blue-800',
  'Qualified': 'bg-green-100 text-green-800',
  'Working': 'bg-yellow-100 text-yellow-800',
  'Nurturing': 'bg-purple-100 text-purple-800',
  'Unqualified': 'bg-red-100 text-red-800',
}

export default function LeadsView() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [showCreateModal, setShowCreateModal] = useState(false)

  const filteredLeads = mockLeads.filter(lead => {
    const matchesSearch = lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.company.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === 'all' || lead.status === statusFilter
    return matchesSearch && matchesStatus
  })

  return (
    <div className="space-y-6">
      {/* Header Actions */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="relative">
            <MagnifyingGlassIcon className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search leads..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input pl-10 w-64"
            />
          </div>
          
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="input w-40"
          >
            <option value="all">All Status</option>
            <option value="New">New</option>
            <option value="Qualified">Qualified</option>
            <option value="Working">Working</option>
            <option value="Nurturing">Nurturing</option>
            <option value="Unqualified">Unqualified</option>
          </select>
        </div>

        <div className="flex items-center space-x-3">
          <button className="btn btn-secondary">
            <FunnelIcon className="h-4 w-4 mr-2" />
            Filters
          </button>
          <button 
            onClick={() => setShowCreateModal(true)}
            className="btn btn-primary"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            New Lead
          </button>
        </div>
      </div>

      {/* Leads Table */}
      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Lead
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Company
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Source
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Created
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                  Last Activity
                </th>
                <th className="relative px-6 py-3">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {filteredLeads.map((lead) => (
                <tr key={lead.id} className="hover:bg-slate-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-slate-900">{lead.name}</div>
                      <div className="text-sm text-slate-500">{lead.email}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                    {lead.company}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${statusColors[lead.status]}`}>
                      {lead.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {lead.source}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {new Date(lead.createdDate).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {new Date(lead.lastActivity).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <Menu as="div" className="relative inline-block text-left">
                      <Menu.Button className="p-2 rounded-lg hover:bg-slate-100">
                        <EllipsisVerticalIcon className="h-5 w-5 text-slate-400" />
                      </Menu.Button>
                      <Transition
                        as={Fragment}
                        enter="transition ease-out duration-100"
                        enterFrom="transform opacity-0 scale-95"
                        enterTo="transform opacity-100 scale-100"
                        leave="transition ease-in duration-75"
                        leaveFrom="transform opacity-100 scale-100"
                        leaveTo="transform opacity-0 scale-95"
                      >
                        <Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                          <div className="py-1">
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`${
                                    active ? 'bg-slate-100' : ''
                                  } flex w-full items-center px-4 py-2 text-sm text-slate-700`}
                                >
                                  <PencilIcon className="h-4 w-4 mr-3" />
                                  Edit Lead
                                </button>
                              )}
                            </Menu.Item>
                            <Menu.Item>
                              {({ active }) => (
                                <button
                                  className={`${
                                    active ? 'bg-slate-100' : ''
                                  } flex w-full items-center px-4 py-2 text-sm text-red-700`}
                                >
                                  <TrashIcon className="h-4 w-4 mr-3" />
                                  Delete Lead
                                </button>
                              )}
                            </Menu.Item>
                          </div>
                        </Menu.Items>
                      </Transition>
                    </Menu>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Results Summary */}
      <div className="flex items-center justify-between text-sm text-slate-500">
        <span>Showing {filteredLeads.length} of {mockLeads.length} leads</span>
        <div className="flex items-center space-x-2">
          <button className="px-3 py-1 rounded border border-slate-300 hover:bg-slate-50">
            Previous
          </button>
          <span className="px-3 py-1">1 of 1</span>
          <button className="px-3 py-1 rounded border border-slate-300 hover:bg-slate-50">
            Next
          </button>
        </div>
      </div>
    </div>
  )
}