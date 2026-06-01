export default function History({ history }) {
  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-6">
      <SectionHeader title="Query History" />

      <div className="bg-card border border-line rounded-2xl p-7">
        <div className="text-[10px] font-mono text-accent tracking-widest uppercase mb-5">
          Recent Queries
        </div>

        {history.length === 0 ? (
          <div className="text-[11px] font-mono text-muted tracking-wider py-4">
            No queries yet. Start asking FitRAG questions.
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {history.map((item, i) => (
              <div key={i} className="bg-bg border border-line rounded-xl px-5 py-4 hover:border-accent/40 transition-all">
                <div className="text-sm text-ink mb-1.5">{item.question}</div>
                <div className="text-[10px] font-mono text-muted tracking-wider">
                  {item.time} · {item.sources?.length || 0} source(s)
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
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