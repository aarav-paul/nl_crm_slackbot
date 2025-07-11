import React from 'react'
import { Fragment } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import {
  HomeIcon,
  UsersIcon,
  SparklesIcon,
  CogIcon,
  XMarkIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline'
import { clsx } from 'clsx'

const navigation = [
  { name: 'Dashboard', id: 'dashboard', icon: HomeIcon },
  { name: 'Leads', id: 'leads', icon: UsersIcon },
  { name: 'AI Assistant', id: 'ai-assistant', icon: SparklesIcon },
  { name: 'Analytics', id: 'analytics', icon: ChartBarIcon },
  { name: 'Settings', id: 'settings', icon: CogIcon },
]

export default function Sidebar({ currentView, setCurrentView, sidebarOpen, setSidebarOpen }) {
  return (
    <>
      {/* Mobile sidebar */}
      <Transition.Root show={sidebarOpen} as={Fragment}>
        <Dialog as="div" className="relative z-50 lg:hidden" onClose={setSidebarOpen}>
          <Transition.Child
            as={Fragment}
            enter="transition-opacity ease-linear duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="transition-opacity ease-linear duration-300"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-slate-900/80" />
          </Transition.Child>

          <div className="fixed inset-0 flex">
            <Transition.Child
              as={Fragment}
              enter="transition ease-in-out duration-300 transform"
              enterFrom="-translate-x-full"
              enterTo="translate-x-0"
              leave="transition ease-in-out duration-300 transform"
              leaveFrom="translate-x-0"
              leaveTo="-translate-x-full"
            >
              <Dialog.Panel className="relative mr-16 flex w-full max-w-xs flex-1">
                <div className="absolute left-full top-0 flex w-16 justify-center pt-5">
                  <button
                    type="button"
                    className="-m-2.5 p-2.5"
                    onClick={() => setSidebarOpen(false)}
                  >
                    <XMarkIcon className="h-6 w-6 text-white" />
                  </button>
                </div>
                <SidebarContent currentView={currentView} setCurrentView={setCurrentView} />
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </Dialog>
      </Transition.Root>

      {/* Static sidebar for desktop */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
        <SidebarContent currentView={currentView} setCurrentView={setCurrentView} />
      </div>
    </>
  )
}

function SidebarContent({ currentView, setCurrentView }) {
  return (
    <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-slate-900 px-6 pb-4">
      <div className="flex h-16 shrink-0 items-center">
        <div className="flex items-center space-x-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-700">
            <SparklesIcon className="h-5 w-5 text-slate-300" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-white">Salesforce AI</h1>
            <p className="text-xs text-slate-400">Lead Management</p>
          </div>
        </div>
      </div>
      
      <nav className="flex flex-1 flex-col">
        <ul role="list" className="flex flex-1 flex-col gap-y-7">
          <li>
            <ul role="list" className="-mx-2 space-y-1">
              {navigation.map((item) => (
                <li key={item.name}>
                  <button
                    onClick={() => setCurrentView(item.id)}
                    className={clsx(
                      currentView === item.id
                        ? 'bg-slate-800 text-white'
                        : 'text-slate-400 hover:text-white hover:bg-slate-800',
                      'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-medium w-full text-left transition-colors'
                    )}
                  >
                    <item.icon className="h-5 w-5 shrink-0" />
                    {item.name}
                  </button>
                </li>
              ))}
            </ul>
          </li>
          
          <li className="mt-auto">
            <div className="rounded-lg bg-slate-800 p-4">
              <div className="flex items-center space-x-3">
                <div className="h-8 w-8 rounded-full bg-slate-700 flex items-center justify-center">
                  <span className="text-sm font-medium text-slate-300">PM</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">Project Manager</p>
                  <p className="text-xs text-slate-400 truncate">Connected to Salesforce</p>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </nav>
    </div>
  )
}