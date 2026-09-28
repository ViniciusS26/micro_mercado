import { useEffect, useState } from 'react'
import { ProdutoEditForm } from './ProdutoEditForm'

interface Produto { id: number; titulo: string; descricao: string; preco: number; peso: number; data_fabricacao: string; data_validade: string }
interface ProdutoListProps { refreshKey: number }
const formatDate = (date: string) => new Date(`${date}T00:00:00`).toLocaleDateString('pt-BR')

export function ProdutoList({ refreshKey }: ProdutoListProps) {
  const [produtos, setProdutos] = useState<Produto[]>([]); 
  
  const [editing, setEditing] = useState<Produto | null>(null);
  
  const [localRefresh, setLocalRefresh] = useState(0); 
  
  const [loading, setLoading] = useState(true); 
  
  const [error, setError] = useState<string | null>(null); 
  
  const [deletingId, setDeletingId] = useState<number | null>(null)
  
  useEffect(() => { 
    let current = true; 
    const load = async () => { setLoading(true); 
        setError(null); 
        
        try { 
            const response = await fetch('http://localhost:8080/api/v1/produtos/'); 
            
            const data = await response.json().catch(() => null); 
            if (!response.ok) throw new Error(data?.detail ?? 'Não foi possível carregar os produtos.'); 
            
            if (current) setProdutos(data) 
        
            } catch (requestError) { 
                if (current) setError(requestError instanceof Error ? requestError.message : 'Erro ao carregar os produtos.') 
            } finally { 
                if (current) setLoading(false) } }; load(); 
                
                return () => { current = false }

            }, [refreshKey, localRefresh])
    const remove = async (produto: Produto) => {
        if (!window.confirm(`Excluir o produto ${produto.titulo}?`)) 
            return; 
        setDeletingId(produto.id); 
        setError(null);
        try { const response = await fetch(`http://localhost:8080/api/v1/produtos/${produto.id}`, { method: 'DELETE' });
            const data = response.ok ? null : await response.json().catch(() => null); 
            
            if (!response.ok) 
                throw new Error(data?.detail ?? 'Não foi possível excluir o produto.'); 
            setEditing(null); 
            setLocalRefresh((value) => value + 1) 
        } catch (requestError) { 
            
            setError(requestError instanceof Error ? requestError.message : 'Erro ao excluir o produto.') 
        } finally { setDeletingId(null) } 
    }
    return <section className="mt-10 border-t border-slate-700 pt-8">
        <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
            <div>
                <h2 className="text-xl font-bold text-white">Produtos cadastrados</h2>
                <p className="mt-1 text-sm text-slate-400">Dados retornados pela API de produtos.</p>
            </div>{!loading && <span className="text-sm text-slate-400">{produtos.length} cadastro(s)</span>}
        </div>{
            editing && <ProdutoEditForm produto={editing} 
            onCancel={
                () => setEditing(null)
            } onSuccess={
                () => { 
                    setEditing(null);
                    setLocalRefresh((value) => value + 1) 
                }
            } />}{
                    loading && <p className="text-slate-300">Carregando produtos...</p>
                }
                {
                    error && <p className="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300" role="alert">{error}</p>}
                {
                    !loading && !error && produtos.length === 0 && <p className="rounded-md border border-slate-700 bg-slate-900/60 p-4 text-slate-300">Nenhum produto cadastrado.</p>}
                {
                    !loading && !error && produtos.length > 0 && <div className="overflow-x-auto rounded-md border border-slate-700">
                        <table className="min-w-full divide-y divide-slate-700 text-left text-sm">
                            <thead className="bg-slate-900/80 text-xs uppercase tracking-wide text-slate-400">
                            <tr>
                                <th className="px-4 py-3">Título</th>
                                <th className="px-4 py-3">Preço</th>
                                <th className="px-4 py-3">Peso</th>
                                <th className="px-4 py-3">Validade</th>
                                <th className="px-4 py-3">Ações</th>
                            </tr>
                            </thead>
                                <tbody className="divide-y divide-slate-700 bg-slate-800 text-slate-200">
                                    {produtos.map((produto) => <tr key={produto.id} className="hover:bg-slate-700/50">
                                    <td className="px-4 py-3">
                                        <p className="font-medium">{produto.titulo}</p>
                                        <p className="max-w-xs truncate text-xs text-slate-400">{produto.descricao}</p>
                                    </td>
                                        <td className="whitespace-nowrap px-4 py-3">{produto.preco.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
                                        <td className="whitespace-nowrap px-4 py-3">{produto.peso}</td><td className="whitespace-nowrap px-4 py-3">{formatDate(produto.data_validade)}</td>
                                        <td className="whitespace-nowrap px-4 py-3">
                                            <div className="flex gap-2">
                                                <button type="button" onClick={() => setEditing(produto)} className="rounded-md bg-slate-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-slate-500">
                                                    Editar
                                                </button>
                                                <button type="button" onClick={() => remove(produto)} disabled={deletingId === produto.id} className="rounded-md bg-red-500/80 px-3 py-1.5 text-xs font-semibold text-white hover:bg-red-500 disabled:opacity-60">
                                                    {deletingId === produto.id ? 'Excluindo...' : 'Excluir'}
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                    )}
                                </tbody>
                        </table>
            </div>
    }</section>
}