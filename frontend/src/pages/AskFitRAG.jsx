import { useState } from 'react'
import axios from 'axios'

const API = 'http://127.0.0.1:8000'

export default function AskFitRAG({ profile, addToHistory }) {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState(null)
  const [loading, setLoading] = useState(false)
  const [useProfile, setUseProfile] = useState(false)

  const ask = async () => {
    if (!question.trim()) return
    setLoading(true)
    setAnswer(null)
    try {
      const res = await axios.post(`${API}/api/ask`, {
        question,
        user_profile: (useProfile && profile) ? profile : {},
      })
      setAnswer(res.data)
      addToHistory({
        question,
        sources: res.data.sources,
        time: new Date().toLocaleTimeString(),
      })
    } catch (e) {
      setAnswer({ error: 'API unreachable. Start uvicorn first.' })
    }
    setLoading(false)
  }

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-6">
      <SectionHeader title="Ask FitRAG" />

      <div className="bg-card border border-line rounded-2xl p-7">
        <div className="text-[10px] font-mono text-accent tracking-widest uppercase mb-4">
          Personalized Query
        </div>

        <textarea
          className="w-full bg-bg border border-line rounded-xl px-4 py-3.5 text-sm outline-none focus:border-accent transition-colors resize-none leading-relaxed"
          rows="3"
          placeholder="Ask anything about recovery, sleep, HRV, nutrition, performance..."
          value={question}
          onChange={e => setQuestion(e.target.value)}
        />

        <div className="mt-4 pt-4 border-t border-line flex items-center justify-between">
          <button
            onClick={() => setUseProfile(!useProfile)}
            className={`text-[10px] font-mono tracking-wider px-3 py-2 rounded-lg border transition-all ${
              useProfile
                ? 'border-good text-good bg-good/5'
                : 'border-line text-muted hover:border-accent hover:text-accent'
            }`}
          >
            {useProfile ? 'PROFILE ACTIVE ✓' : 'USE MY PROFILE'}
          </button>
          <span className="text-[10px] font-mono text-muted tracking-wider">
            {profile ? 'Profile available' : 'No profile saved'}
          </span>
        </div>

        <div className="flex justify-end mt-5">
          <button
            onClick={ask}
            disabled={loading}
            className="bg-accent text-white rounded-xl px-7 py-3 text-sm font-semibold hover:opacity-90 transition-opacity disabled:opacity-40"
          >
            Run Query →
          </button>
        </div>
      </div>

      {loading && (
        <div className="bg-card border border-line rounded-2xl p-7 flex items-center gap-3">
          <Dots />
          <span className="text-xs font-mono text-muted tracking-wide">
            EMBEDDING · SEARCHING CHROMADB · GENERATING
          </span>
        </div>
      )}

      {answer && <AnswerCard answer={answer} />}
    </div>
  )
}

function SectionHeader({ title }) {
  return (
    <div className="flex items-center gap-3">
      <h2 className="text-base font-semibold">{title}</h2>
      <div className="flex-1 h-px bg-line" />
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