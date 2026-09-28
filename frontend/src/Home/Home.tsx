interface HomeProps {
  onLogout: () => void
}

export function Home({ onLogout }: HomeProps) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-900 p-4 text-white">
      <section className="w-full max-w-3xl rounded-lg border border-slate-700 bg-slate-800 p-8 shadow-xl">
        <header className="flex items-center justify-between gap-4 border-b border-slate-700 pb-6">
          <div>
            <p className="text-sm font-semibold uppercase tracking-widest text-emerald-400">SGM</p>
            <h1 className="mt-2 text-3xl font-bold">Início</h1>
          </div>
          <button
            type="button"
            onClick={onLogout}
            className="rounded-md border border-slate-600 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            Sair
          </button>
        </header>
        <p className="pt-6 text-slate-300">Login realizado com sucesso.</p>
      </section>

      <section>
        
      </section>


    </main>
  )
}