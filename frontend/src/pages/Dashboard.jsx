import { useState } from 'react'
import axios from 'axios'

const API = 'http://127.0.0.1:8000'

export default function Dashboard({ profile, addToHistory }) {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)

  const ask = async () => {
    if (!question.trim()) return
    setLoading(true)
    setAnswer(null)
    try {
      const res = await axios.post(`${API}/api/ask`, {
        question,
        user_profile: profile || {},
      })
      setAnswer(res.data)
      addToHistory({
        question,
        sources: res.data.sources,
        time: new Date().toLocaleTimeString(),
      })
    } catch (e) {
      setAnswer({ error: 'Could not reach FitRAG API. Make sure uvicorn is running on port 8000.' })
    }
    setLoading(false)
  }

  return (
    <div className="max-w-5xl mx-auto flex flex-col gap-6">
      {/* Hero */}
      <div className="bg-card border border-line rounded-2xl p-10">
        <div className="text-[10px] font-mono text-accent tracking-widest uppercase mb-3">
          Recovery Intelligence Platform
        </div>
        <h1 className="text-4xl font-extrabold leading-tight mb-3">
          Understand your body<br />with <span className="text-accent">real science</span>
        </h1>
        <p className="text-sm text-muted max-w-md leading-relaxed">
          Ask any recovery, sleep, or performance question and get answers backed by peer-reviewed research, personalized to your data.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <StatCard label="KNOWLEDGE BASE" value="2,441" sub="indexed vectors" color="accent" />
        <StatCard label="RESEARCH PAPERS" value="14" sub="peer-reviewed" color="good" />
        <StatCard label="EMBEDDING DIM" value="384" sub="vector size" color="amber" />
        <StatCard label="API STATUS" value="Live" sub="port 8000" color="good" />
      </div>

      {/* Quick Ask */}
      <div className="bg-card border border-line rounded-2xl p-7">
        <div className="text-[10px] font-mono text-accent tracking-widest uppercase mb-4">
          Quick Ask
        </div>
        <div className="flex gap-3">
          <input
            className="flex-1 bg-bg border border-line rounded-xl px-4 py-3.5 text-sm outline-none focus:border-accent transition-colors"
            placeholder="e.g. Why is my recovery low after drinking alcohol?"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && ask()}
          />
          <button
            onClick={ask}
            disabled={loading}
            className="bg-accent text-white rounded-xl px-6 py-3.5 text-sm font-semibold hover:opacity-90 transition-opacity disabled:opacity-40"
          >
            Ask →
          </button>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="bg-card border border-line rounded-2xl p-7 flex items-center gap-3">
          <Dots />
          <span className="text-xs font-mono text-muted tracking-wide">
            RETRIEVING RESEARCH · GENERATING ANSWER
          </span>
        </div>
      )}

      {/* Answer */}
      {answer && <AnswerCard answer={answer} />}
    </div>
  )
}

function StatCard({ label, value, sub, color }) {
  const bar = {
    accent: 'bg-accent',
    good: 'bg-good',
    amber: 'bg-amber',
  }
  return (
    <div className="bg-card border border-line rounded-xl p-5 relative overflow-hidden">
      <div className={`absolute top-0 left-0 right-0 h-1 ${bar[color]}`} />
      <div className="text-[9px] font-mono text-muted tracking-widest uppercase mb-2.5">{label}</div>
      <div className="text-3xl font-extrabold leading-none mb-1">{value}</div>
      <div className="text-[11px] font-mono text-muted">{sub}</div>
    </div>
  )
}

function AnswerCard({ answer }) {
  if (answer.error) {
    return (
      <div className="bg-low/5 border border-low/20 rounded-xl px-4 py-3 text-xs font-mono text-low">
        ERROR: {answer.error}
      </div>
    )
  }
  return (
    <div className="bg-card border border-line rounded-2xl p-7">
      <div className="text-xs font-mono text-muted mb-5 pb-4 border-b border-line">
        <span className="text-ink">Q:</span> {answer.question}
      </div>
      <div className="text-sm text-ink/80 leading-7 whitespace-pre-wrap">
        {answer.answer}
      </div>
      {answer.sources?.length > 0 && (
        <div className="mt-5 pt-4 border-t border-line">
          <div className="text-[9px] font-mono text-muted tracking-widest uppercase mb-2.5">Sources</div>
          <div className="flex flex-wrap gap-2">
            {answer.sources.map((s, i) => (
              <span key={i} className="text-[10px] font-mono text-accent bg-accent/5 border border-accent/15 rounded px-2.5 py-1">
                {s.replace('.pdf', '')}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function Dots() {
  return (
    <div className="flex gap-1">
      {[0, 1, 2].map(i => (
        <span
          key={i}
          className="w-1.5 h-1.5 rounded-full bg-accent animate-bounce"
          style={{ animationDelay: `${i * 0.15}s` }}
        />
      ))}
    </div>
  )
}