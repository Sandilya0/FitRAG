import { useState } from 'react'
import axios from 'axios'

const API = 'http://127.0.0.1:8000'

export default function WhoopData({ whoopProfile, setWhoopProfile, setProfile }) {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    setLoading(true)
    setStatus(null)
    const formData = new FormData()
    formData.append('file', file)
    try {
      const res = await axios.post(`${API}/api/upload/whoop`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setWhoopProfile(res.data.profile)
      setStatus({ ok: true, msg: 'WHOOP DATA LOADED SUCCESSFULLY' })
    } catch (err) {
      setStatus({ ok: false, msg: 'Could not upload WHOOP data.' })
    }
    setLoading(false)
  }

  const metrics = whoopProfile ? [
    { label: 'RECOVERY', value: whoopProfile.recovery_score ? Math.round(whoopProfile.recovery_score) + '%' : 'N/A',
      color: recoveryColor(whoopProfile.recovery_score) },
    { label: 'HRV', value: whoopProfile.hrv ? Math.round(whoopProfile.hrv) + 'ms' : 'N/A', color: 'accent' },
    { label: 'RESTING HR', value: whoopProfile.resting_hr ? Math.round(whoopProfile.resting_hr) + ' bpm' : 'N/A', color: 'ink' },
    { label: 'SLEEP', value: whoopProfile.sleep_duration ? whoopProfile.sleep_duration + 'h' : 'N/A', color: 'ink' },
    { label: 'SLEEP QUALITY', value: whoopProfile.sleep_quality || 'N/A', color: 'ink' },
    { label: 'STRAIN', value: whoopProfile.exercise_intensity || 'N/A', color: 'ink' },
  ] : []

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-6">
      <SectionHeader title="WHOOP Integration" />

      {/* Upload */}
      <div className="bg-card border border-line rounded-2xl p-7">
        <div className="text-[10px] font-mono text-accent tracking-widest uppercase mb-5">
          Upload WHOOP Export
        </div>

        <label className="block border-2 border-dashed border-line rounded-xl p-10 text-center cursor-pointer hover:border-accent hover:bg-accent/5 transition-all">
          <svg className="w-10 h-10 mx-auto mb-3 text-muted" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          <div className="text-sm text-muted mb-1.5">Click to upload your WHOOP CSV</div>
          <div className="text-[10px] font-mono text-muted tracking-wider">
            physiological_cycles.csv
          </div>
          <input type="file" accept=".csv" className="hidden" onChange={handleUpload} />
        </label>

        {loading && (
          <div className="mt-4 flex items-center gap-3">
            <Dots />
            <span className="text-xs font-mono text-muted tracking-wide">PARSING WHOOP DATA</span>
          </div>
        )}

        {status && (
          <div className={`mt-4 text-[10px] font-mono tracking-wider ${status.ok ? 'text-good' : 'text-low'}`}>
            {status.msg}
          </div>
        )}
      </div>

      {/* Metrics */}
      {whoopProfile && (
        <div className="bg-card border border-line rounded-2xl p-7">
          <div className="text-[10px] font-mono text-accent tracking-widest uppercase mb-5">
            Latest Metrics
          </div>
          <div className="grid grid-cols-3 gap-4">
            {metrics.map(m => (
              <MetricCard key={m.label} {...m} />
            ))}
          </div>
          <div className="mt-6">
            <button
              onClick={() => setProfile(whoopProfile)}
              className="bg-accent text-white rounded-xl px-7 py-3 text-sm font-semibold hover:opacity-90 transition-opacity"
            >
              Use This Data in Queries →
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

function MetricCard({ label, value, color }) {
  const colors = {
    good: 'text-good',
    amber: 'text-amber',
    low: 'text-low',
    accent: 'text-accent',
    ink: 'text-ink',
  }
  return (
    <div className="bg-bg border border-line rounded-xl p-5 text-center">
      <div className={`text-3xl font-extrabold leading-none mb-1.5 ${colors[color]}`}>{value}</div>
      <div className="text-[9px] font-mono text-muted tracking-widest uppercase">{label}</div>
    </div>
  )
}

function recoveryColor(score) {
  if (!score) return 'ink'
  if (score > 66) return 'good'
  if (score > 33) return 'amber'
  return 'low'
}

function SectionHeader({ title }) {
  return (
    <div className="flex items-center gap-3">
      <h2 className="text-base font-semibold">{title}</h2>
      <div className="flex-1 h-px bg-line" />
    </div>
  )
}

function Dots() {
  return (
    <div className="flex gap-1">
      {[0, 1, 2].map(i => (
        <span key={i} className="w-1.5 h-1.5 rounded-full bg-accent animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
      ))}
    </div>
  )
}