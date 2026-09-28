import './Header.css'

interface HomeProps {
  activeSection: string
  onSelectSection: (section: string) => void
  onLogout: () => void
}

const menuItems = [
  { id: 'inicio', label: 'Início' },
  { id: 'fornecedor', label: 'Funcionários', subItems: [{ id: 'fornecedor-cadastrar', label: 'Cadastrar funcionário' }, { id: 'fornecedor-listar', label: 'Listar funcionários' }] },
  { id: 'produtos', label: 'Produtos', subItems: [{ id: 'produtos-cadastrar', label: 'Cadastrar produto' }, { id: 'produtos-listar', label: 'Listar produtos' }] },
  { id: 'vendas', label: 'Vendas', subItems: [{ id: 'vendas-cadastrar', label: 'Cadastrar venda' }, { id: 'vendas-listar', label: 'Listar vendas' }] },
]

function Header({ activeSection, onSelectSection, onLogout }: HomeProps){
    return(
        <aside className="header w-full flex-shrink-0 border-b border-slate-700 bg-slate-800 p-4 md:min-h-screen md:w-64 md:border-b-0 md:border-r">
          <div className="mb-6">
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-emerald-400">Sistema</p>
            <h3 className="mt-1 text-3xl font-bold text-white">SGM</h3>
          </div>
          <nav aria-label="Menu principal" className="flex flex-col gap-2">
            {menuItems.map((item) => {
              const isActive = item.subItems ? activeSection.startsWith(`${item.id}-`) : activeSection === item.id
              return (
              <div key={item.id}>
                <button type="button" onClick={() => onSelectSection(item.subItems ? `${item.id}-listar` : item.id)} className={`w-full rounded-md px-4 py-3 text-left text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-emerald-500 ${isActive ? 'bg-emerald-500 text-slate-950' : 'text-slate-300 hover:bg-slate-700 hover:text-white'}`}>
                  {item.label}
                </button>
                {isActive && item.subItems && (
                <div className="mt-1 ml-3 flex flex-col gap-1 border-l border-slate-600 pl-3">
                  {item.subItems.map((subItem) => (
                    <button
                      key={subItem.id}
                      type="button"
                      onClick={() => onSelectSection(subItem.id)}
                      className={`w-full rounded-md px-3 py-2 text-left text-sm transition focus:outline-none focus:ring-2 focus:ring-emerald-500 ${activeSection === subItem.id ? 'bg-slate-600 text-white' : 'text-slate-400 hover:bg-slate-700 hover:text-white'}`}
                    >
                      {subItem.label}
                    </button>
                  ))}
                </div>
                )}
              </div>
              )
            })}
            <button
              type="button"
              onClick={onLogout}
              className="mt-4 w-full rounded-md border border-slate-600 px-4 py-3 text-left text-sm font-semibold text-slate-200 transition hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              Sair
            </button>
          </nav>
        </aside>
    );
}

export default Header;