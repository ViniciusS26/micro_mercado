import { useState } from 'react'
import type { FormEvent } from 'react'

interface VendaItem { produto_id: number; quantidade: number; titulo_produto: string; preco_unitario: number }
export interface Venda { id: number; funcionario_id: number; nome_funcionario: string; cpf: string; cargo: string; data_venda: string; valor_total: number; itens: VendaItem[] }
const inputClassName = 'w-full rounded-md border border-slate-600 bg-slate-700 px-3 py-2 text-white focus:border-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400'

export function VendaEditForm({ venda, onCancel, onSuccess }: { venda: Venda; onCancel: () => void; onSuccess: () => void }) {
  const [formData, setFormData] = useState({ funcionario_id: String(venda.funcionario_id), nome_funcionario: venda.nome_funcionario, cpf: venda.cpf, cargo: venda.cargo, quantidade: String(venda.itens[0]?.quantidade ?? 1) })
  const [error, setError] = useState<string | null>(null); const [isSubmitting, setIsSubmitting] = useState(false)
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => setFormData((current) => ({ ...current, [event.target.name]: event.target.value }))
  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); setError(null); setIsSubmitting(true)
    try {
      const response = await fetch(`http://localhost:8080/api/v1/vendas/${venda.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ funcionario_id: Number(formData.funcionario_id), nome_funcionario: formData.nome_funcionario, cpf: formData.cpf, cargo: formData.cargo, itens: venda.itens.map((item) => ({ ...item, quantidade: Number(formData.quantidade) })) }) })
      const data = response.ok ? null : await response.json().catch(() => null)
      if (!response.ok) { setError(data?.detail ?? 'Não foi possível atualizar a venda.'); return }
      onSuccess()
    } catch { setError('Não foi possível conectar à API de vendas.') } finally { setIsSubmitting(false) }
  }
  return <form onSubmit={handleSubmit} className="mb-8 rounded-md border border-emerald-500/30 bg-slate-900/60 p-5"><div className="mb-4 flex items-center justify-between"><h3 className="text-lg font-bold text-white">Editar venda #{venda.id}</h3><button type="button" onClick={onCancel} className="text-sm text-slate-400 hover:text-white">Cancelar</button></div><div className="grid gap-4 md:grid-cols-2"><label className="text-sm font-medium text-slate-300">ID do funcionário<input className={inputClassName} type="number" min="1" name="funcionario_id" value={formData.funcionario_id} onChange={handleChange} required /></label><label className="text-sm font-medium text-slate-300">Nome do funcionário<input className={inputClassName} name="nome_funcionario" value={formData.nome_funcionario} onChange={handleChange} required /></label><label className="text-sm font-medium text-slate-300">CPF<input className={inputClassName} name="cpf" value={formData.cpf} onChange={handleChange} required /></label><label className="text-sm font-medium text-slate-300">Cargo<input className={inputClassName} name="cargo" value={formData.cargo} onChange={handleChange} required /></label><label className="text-sm font-medium text-slate-300">Quantidade<input className={inputClassName} type="number" min="1" name="quantidade" value={formData.quantidade} onChange={handleChange} required /></label></div>{error && <p className="mt-4 rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300" role="alert">{error}</p>}<button type="submit" disabled={isSubmitting} className="mt-5 rounded-md bg-emerald-500 px-4 py-2 font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-60">{isSubmitting ? 'Salvando...' : 'Salvar alterações'}</button></form>
}