import { useState } from 'react'
import type { FormEvent } from 'react'

interface ProdutoFormData {
  titulo: string
  descricao: string
  preco: string
  peso: string
  data_fabricacao: string
  data_validade: string
}

const initialFormData: ProdutoFormData = {
  titulo: '', descricao: '', preco: '', peso: '', data_fabricacao: '', data_validade: '',
}

const inputClassName = 'w-full rounded-md border border-slate-600 bg-slate-700 px-3 py-2 text-white placeholder-slate-400 focus:border-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400'

function getErrorMessage(errorData: { detail?: string | { msg?: string }[] } | null, fallback: string) {
  if (Array.isArray(errorData?.detail)) return errorData.detail.map((error) => error.msg ?? 'Valor inválido').join('; ')
  return errorData?.detail ?? fallback
}

interface ProdutoFormProps { onSuccess?: () => void }

export function ProdutoForm({ onSuccess }: ProdutoFormProps) {
  const [formData, setFormData] = useState(initialFormData)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target
    setFormData((currentData) => ({ ...currentData, [name]: value }))
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    setSuccess(null)
    setIsSubmitting(true)

    try {
      const response = await fetch('http://localhost:8080/api/v1/produtos/', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, preco: Number(formData.preco), peso: Number(formData.peso) }),
      })
      const errorData = response.ok ? null : await response.json().catch(() => null)
      if (!response.ok) { setError(getErrorMessage(errorData, 'Não foi possível cadastrar o produto.')); return }
      setFormData(initialFormData)
      setSuccess('Produto cadastrado com sucesso.')
      onSuccess?.()
    } catch { setError('Não foi possível conectar à API de produtos.') } finally { setIsSubmitting(false) }
  }

  return (
    <form onSubmit={handleSubmit} className="mt-8 grid gap-5 md:grid-cols-2">
      <label className="text-sm font-medium text-slate-300">Título<input className={inputClassName} name="titulo" value={formData.titulo} onChange={handleChange} required /></label>
      <label className="text-sm font-medium text-slate-300">Preço<input className={inputClassName} type="number" min="0" step="0.01" name="preco" value={formData.preco} onChange={handleChange} required /></label>
      <label className="text-sm font-medium text-slate-300">Peso<input className={inputClassName} type="number" min="0" step="0.01" name="peso" value={formData.peso} onChange={handleChange} required /></label>
      <label className="text-sm font-medium text-slate-300">Data de fabricação<input className={inputClassName} type="date" name="data_fabricacao" value={formData.data_fabricacao} onChange={handleChange} required /></label>
      <label className="text-sm font-medium text-slate-300">Data de validade<input className={inputClassName} type="date" name="data_validade" value={formData.data_validade} onChange={handleChange} required /></label>
      <label className="text-sm font-medium text-slate-300 md:col-span-2">Descrição<textarea className={inputClassName} name="descricao" value={formData.descricao} onChange={handleChange} rows={3} required /></label>
      {error && <p className="md:col-span-2 rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300" role="alert">{error}</p>}
      {success && <p className="md:col-span-2 rounded-md border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-300" role="status">{success}</p>}
      <button type="submit" disabled={isSubmitting} className="w-full rounded-md bg-emerald-500 px-4 py-2 font-semibold text-slate-950 hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-60 md:col-span-2">{isSubmitting ? 'Cadastrando...' : 'Cadastrar produto'}</button>
    </form>
  )
}