import { NavLink } from 'react-router-dom'

const navItems = [
  { to: '/', label: 'Dashboard', icon: GridIcon },
  { to: '/ask', label: 'Ask FitRAG', icon: ChatIcon },
  { to: '/profile', label: 'My Profile', icon: UserIcon },
  { to: '/whoop', label: 'WHOOP Data', icon: PulseIcon },
  { to: '/history', label: 'History', icon: ClockIcon },
]

export default function Sidebar() {
  return (
    <aside className="w-64 min-w-64 bg-card border-r border-line flex flex-col">
      {/* Logo */}
      <div className="px-6 py-7 border-b border-line">
        <div className="text-2xl font-extrabold tracking-tight">
          Fit<span className="text-accent">RAG</span>
        </div>
        <div className="text-[10px] font-mono text-muted tracking-widest uppercase mt-1">
          Recovery Intelligence
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 py-4 flex flex-col gap-1">
        {navItems.map(item => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all ${
                isActive
                  ? 'bg-bg text-ink font-medium'
                  : 'text-muted hover:bg-bg hover:text-ink'
              }`
            }
          >
            <item.icon />
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* Footer stats */}
      <div className="px-6 py-5 border-t border-line">
        <div className="flex flex-col gap-2">
          <Stat label="VECTORS" value="2,441" />
          <Stat label="PAPERS" value="14" />
          <Stat label="MODEL" value="LLAMA-3.3" />
        </div>
      </div>
    </aside>
  )
}

function Stat({ label, value }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-[10px] font-mono text-muted tracking-wider">{label}</span>
      <span className="text-[10px] font-mono text-good">{value}</span>
    </div>
  )
}

// Icons
function GridIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/>
      <rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>
    </svg>
  )
}

function ChatIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
    </svg>
  )
}

function UserIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
    </svg>
  )
}

function PulseIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
    </svg>
  )
}

function ClockIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
    </svg>
  )
}