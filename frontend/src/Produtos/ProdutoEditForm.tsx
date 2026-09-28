import { useState } from 'react'
import type { FormEvent } from 'react'

interface ProdutoEdit { id: number; titulo: string; descricao: string; preco: number; peso: number }
interface ProdutoEditFormProps { produto: ProdutoEdit; onCancel: () => void; onSuccess: () => void }
const inputClassName = 'w-full rounded-md border border-slate-600 bg-slate-700 px-3 py-2 text-white focus:border-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400'

export function ProdutoEditForm({ produto, onCancel, onSuccess }: ProdutoEditFormProps) {
  const [formData, setFormData] = useState({ titulo: produto.titulo, descricao: produto.descricao, preco: String(produto.preco), peso: String(produto.peso) })
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => setFormData((current) => ({ ...current, [event.target.name]: event.target.value }))
  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); setError(null); setIsSubmitting(true)
    try {
      const response = await fetch(`http://localhost:8080/api/v1/produtos/${produto.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ...formData, preco: Number(formData.preco), peso: Number(formData.peso) }) })
      const data = response.ok ? null : await response.json().catch(() => null)
      if (!response.ok) { setError(data?.detail ?? 'Não foi possível atualizar o produto.'); return }
      onSuccess()
    } catch { setError('Não foi possível conectar à API de produtos.') } finally { setIsSubmitting(false) }
  }
  return <form onSubmit={handleSubmit} className="mb-8 rounded-md border border-emerald-500/30 bg-slate-900/60 p-5"><div className="mb-4 flex items-center justify-between"><h3 className="text-lg font-bold text-white">Editar produto</h3><button type="button" onClick={onCancel} className="text-sm text-slate-400 hover:text-white">Cancelar</button></div><div className="grid gap-4 md:grid-cols-2"><label className="text-sm font-medium text-slate-300">Título<input className={inputClassName} name="titulo" value={formData.titulo} onChange={handleChange} required /></label><label className="text-sm font-medium text-slate-300">Preço<input className={inputClassName} type="number" min="0" step="0.01" name="preco" value={formData.preco} onChange={handleChange} required /></label><label className="text-sm font-medium text-slate-300">Peso<input className={inputClassName} type="number" min="0" step="0.01" name="peso" value={formData.peso} onChange={handleChange} required /></label><label className="text-sm font-medium text-slate-300 md:col-span-2">Descrição<textarea className={inputClassName} name="descricao" value={formData.descricao} onChange={handleChange} rows={3} required /></label></div>{error && <p className="mt-4 rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300" role="alert">{error}</p>}<button type="submit" disabled={isSubmitting} className="mt-5 rounded-md bg-emerald-500 px-4 py-2 font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60">{isSubmitting ? 'Salvando...' : 'Salvar alterações'}</button></form>
}