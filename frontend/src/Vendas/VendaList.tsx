import { useEffect, useState } from 'react'
import { VendaEditForm } from './VendaEditForm'
import type { Venda } from './VendaEditForm'

interface VendaListProps { refreshKey: number }
const formatDate = (date: string) => new Date(date).toLocaleDateString('pt-BR')

export function VendaList({ refreshKey }: VendaListProps) {
    const [vendas, setVendas] = useState<Venda[]>([]);
    const [editing, setEditing] = useState<Venda | null>(null); const [localRefresh, setLocalRefresh] = useState(0); const [loading, setLoading] = useState(true); const [error, setError] = useState<string | null>(null); const [deletingId, setDeletingId] = useState<number | null>(null)
    useEffect(() => { 
        let current = true; 
        const load = async () => { 
            setLoading(true); 
            setError(null); 
            try { 
                
                const response = await fetch('http://localhost:8080/api/v1/vendas/'); 
                
                const data = await response.json().catch(() => null); 
                
                if (!response.ok) 
                    throw new Error(data?.detail ?? 'Não foi possível carregar as vendas.'); 
                
                if (current) 
                    setVendas(data.vendas ?? []) 
            } catch (requestError) { 
                if (current) 
                    setError(requestError instanceof Error ? requestError.message : 'Erro ao carregar as vendas.') 
                } finally { if (current) setLoading(false) } 
            }; 
            
            load(); 
            
            return () => { 
                current = false 
            } 
        }, [refreshKey, localRefresh]
    )
    const remove = async (venda: Venda) => {
        if (!window.confirm(`Excluir a venda #${venda.id}?`))
            return; 
        setDeletingId(venda.id); 
        setError(null); 
        
        try {
            const response = await fetch(`http://localhost:8080/api/v1/vendas/${venda.id}`, { method: 'DELETE' }); 
            
            const data = response.ok ? null : await response.json().catch(() => null); 
            
            if (!response.ok) 
                throw new Error(data?.detail ?? 'Não foi possível excluir a venda.');
                setEditing(null); 
                setLocalRefresh((value) => value + 1) 
        } catch (requestError) { 
            setError(requestError instanceof Error ? requestError.message : 'Erro ao excluir a venda.') 
        } finally { setDeletingId(null) 

        } 
    }
  return <section className="mt-10 border-t border-slate-700 pt-8">
    <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
        <div>
            <h2 className="text-xl font-bold text-white">Vendas cadastradas</h2>
            <p className="mt-1 text-sm text-slate-400">Dados retornados pela API de vendas.</p>
        </div>{!loading && 
            <span className="text-sm text-slate-400">{vendas.length} venda(s)</span>}
        </div>
        {editing && <VendaEditForm venda={editing} onCancel={() => setEditing(null)} onSuccess={() => { setEditing(null); setLocalRefresh((value) => value + 1) }} />}{loading && <p className="text-slate-300">Carregando vendas...</p>}{error && <p className="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300" role="alert">{error}</p>}{!loading && !error && vendas.length === 0 && <p className="rounded-md border border-slate-700 bg-slate-900/60 p-4 text-slate-300">Nenhuma venda cadastrada.</p>}{!loading && !error && vendas.length > 0 && <div className="overflow-x-auto rounded-md border border-slate-700"><table className="min-w-full divide-y divide-slate-700 text-left text-sm"><thead className="bg-slate-900/80 text-xs uppercase tracking-wide text-slate-400"><tr><th className="px-4 py-3">Venda</th><th className="px-4 py-3">Funcionário</th><th className="px-4 py-3">Itens</th><th className="px-4 py-3">Total</th><th className="px-4 py-3">Data</th><th className="px-4 py-3">Ações</th></tr></thead><tbody className="divide-y divide-slate-700 bg-slate-800 text-slate-200">{vendas.map((venda) => <tr key={venda.id} className="hover:bg-slate-700/50"><td className="whitespace-nowrap px-4 py-3 font-medium">#{venda.id}</td><td className="px-4 py-3">{venda.nome_funcionario}<span className="block text-xs text-slate-400">{venda.cargo}</span></td><td className="px-4 py-3">{venda.itens.map((item) => `${item.titulo_produto} (${item.quantidade})`).join(', ')}</td><td className="whitespace-nowrap px-4 py-3">{venda.valor_total.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td><td className="whitespace-nowrap px-4 py-3">{formatDate(venda.data_venda)}</td><td className="whitespace-nowrap px-4 py-3"><div className="flex gap-2"><button type="button" onClick={() => setEditing(venda)} className="rounded-md bg-slate-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-slate-500">Editar</button><button type="button" onClick={() => remove(venda)} disabled={deletingId === venda.id} className="rounded-md bg-red-500/80 px-3 py-1.5 text-xs font-semibold text-white hover:bg-red-500 disabled:opacity-60">{deletingId === venda.id ? 'Excluindo...' : 'Excluir'}</button></div></td></tr>)}</tbody></table></div>}</section>
}