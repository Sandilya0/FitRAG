import { useState } from 'react'

const FACTORS = ['Late night eating', 'Caffeine after 3pm', 'Lots of screen time', 'Illness/sickness']

export default function Profile({ profile, setProfile }) {
  const [form, setForm] = useState({
    sleep_duration: profile?.sleep_duration || '',
    sleep_quality: profile?.sleep_quality || '',
    alcohol: profile?.alcohol ? 'Yes' : 'No',
    stress: profile?.stress || '',
    exercise: profile?.exercise || 'No',
    exercise_intensity: profile?.exercise_intensity || 'moderate',
    feeling: profile?.feeling || '',
  })
  const [factors, setFactors] = useState(profile?.additional_factors || [])
  const [saved, setSaved] = useState(false)

  const update = (key, value) => setForm(prev => ({ ...prev, [key]: value }))

  const toggleFactor = (f) => {
    setFactors(prev => prev.includes(f) ? prev.filter(x => x !== f) : [...prev, f])
  }

  const save = () => {
    setProfile({
      ...form,
      alcohol: form.alcohol === 'Yes',
      additional_factors: factors,
    })
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  const clear = () => {
    setForm({
      sleep_duration: '', sleep_quality: '', alcohol: 'No',
      stress: '', exercise: 'No', exercise_intensity: 'moderate', feeling: '',
    })
    setFactors([])
    setProfile(null)
  }

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-6">
      <SectionHeader title="My Health Profile" />

      <div className="bg-card border border-line rounded-2xl p-7">
        <div className="text-[10px] font-mono text-accent tracking-widest uppercase mb-5">
          Today's Status
        </div>

        <div className="grid grid-cols-2 gap-5">
          <Select label="Sleep Duration" value={form.sleep_duration} onChange={v => update('sleep_duration', v)}
            options={['Less than 6hrs', '6-7hrs', '7-8hrs', '8hrs+']} />
          <Select label="Sleep Quality" value={form.sleep_quality} onChange={v => update('sleep_quality', v)}
            options={['Poor', 'Average', 'Good', 'Great']} />
          <Select label="Alcohol Yesterday" value={form.alcohol} onChange={v => update('alcohol', v)}
            options={['No', 'Yes']} />
          <Select label="Stress Level" value={form.stress} onChange={v => update('stress', v)}
            options={['Low', 'Moderate', 'High']} />
          <Select label="Exercise Yesterday" value={form.exercise} onChange={v => update('exercise', v)}
            options={['No', 'Yes']} />
          <Select label="Exercise Intensity" value={form.exercise_intensity} onChange={v => update('exercise_intensity', v)}
            options={['light', 'moderate', 'heavy']} />
          <Select label="How You Feel" value={form.feeling} onChange={v => update('feeling', v)}
            options={['Terrible', 'Tired', 'Okay', 'Good', 'Great']} />
        </div>

        <div className="mt-6">
          <div className="text-[10px] font-mono text-muted tracking-widest uppercase mb-3">
            Additional Factors
          </div>
          <div className="flex flex-wrap gap-2">
            {FACTORS.map(f => (
              <button
                key={f}
                onClick={() => toggleFactor(f)}
                className={`text-xs px-3 py-2 rounded-lg border transition-all ${
                  factors.includes(f)
                    ? 'border-accent text-accent bg-accent/5'
                    : 'border-line text-muted hover:border-accent/40'
                }`}
              >
                {f}
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-end gap-3 mt-7">
          <button onClick={clear}
            className="text-[11px] font-mono tracking-wider px-5 py-3 rounded-xl border border-line text-muted hover:border-accent hover:text-accent transition-all">
            CLEAR
          </button>
          <button onClick={save}
            className="bg-accent text-white rounded-xl px-7 py-3 text-sm font-semibold hover:opacity-90 transition-opacity">
            Save Profile →
          </button>
        </div>

        {saved && (
          <div className="mt-4 text-[10px] font-mono text-good tracking-wider">
            PROFILE SAVED SUCCESSFULLY
          </div>
        )}
      </div>
    </div>
  )
}

function Select({ label, value, onChange, options }) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-[10px] font-mono text-muted tracking-wider uppercase">{label}</label>
      <select
        value={value}
        onChange={e => onChange(e.target.value)}
        className="bg-bg border border-line rounded-lg px-3 py-2.5 text-sm outline-none focus:border-accent transition-colors appearance-none cursor-pointer"
      >
        <option value="">Select</option>
        {options.map(o => <option key={o} value={o}>{o}</option>)}
      </select>
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