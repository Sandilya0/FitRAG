import { useLocation } from 'react-router-dom'

const titles = {
  '/': 'Dashboard',
  '/ask': 'Ask FitRAG',
  '/profile': 'My Profile',
  '/whoop': 'WHOOP Data',
  '/history': 'History',
}

export default function Topbar() {
  const location = useLocation()
  const title = titles[location.pathname] || 'FitRAG'

  return (
    <header className="px-8 py-4 bg-card border-b border-line flex items-center justify-between">
      <div className="text-sm font-semibold text-muted">
        FitRAG <span className="text-line mx-1">/</span>
        <span className="text-ink">{title}</span>
      </div>
      <div className="flex items-center gap-3">
        <Badge color="good" label="GROQ ACTIVE" />
        <Badge color="accent" label="CHROMADB READY" />
      </div>
    </header>
  )
}

function Badge({ color, label }) {
  const colors = {
    good: 'bg-good/10 text-good',
    accent: 'bg-accent/10 text-accent',
  }
  return (
    <span className={`text-[10px] font-mono tracking-wider px-2.5 py-1 rounded ${colors[color]}`}>
      {label}
    </span>
  )
}