import './Header.css'

interface HomeProps {
  onLogout: () => void
}


function Header({ onLogout }: HomeProps){
    return(
        <header className="header flex items-center justify-between gap-2 border-b border-slate-700 pb-6 p-2">
          <div>
            <h3 className="mt-2 text-3xl font-bold">Início</h3>
          </div>
          <button
            type="button"
            onClick={onLogout}
            className="rounded-md border border-slate-600 px-4 py-2 text-sm font-semibold text-slate-200 transition hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            Sair
          </button>
        </header>
    );
}

export default Header;