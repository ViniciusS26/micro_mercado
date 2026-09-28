import { useState } from 'react'
import type { FormEvent } from 'react'

interface EditableFuncionario {
  id: number
  nome: string
  email: string
  telefone: string
  cargo: string
  salario: number
}

interface FuncionarioEditFormProps {
  funcionario: EditableFuncionario
  onCancel: () => void
  onSuccess: () => void
}

interface EditFormData {
  nome: string
  email: string
  telefone: string
  cargo: string
  salario: string
}

const inputClassName = 'w-full rounded-md border border-slate-600 bg-slate-700 px-3 py-2 text-white placeholder-slate-400 focus:border-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400'

function getErrorMessage(errorData: { detail?: string | { msg?: string }[] } | null) {
  if (Array.isArray(errorData?.detail)) {
    return errorData.detail.map((error) => error.msg ?? 'Valor inválido').join('; ')
  }

  return errorData?.detail ?? 'Não foi possível atualizar o funcionário.'
}

export function FuncionarioEditForm({ funcionario, onCancel, onSuccess }: FuncionarioEditFormProps) {
  const [formData, setFormData] = useState<EditFormData>({
    nome: funcionario.nome,
    email: funcionario.email,
    telefone: funcionario.telefone,
    cargo: funcionario.cargo,
    salario: String(funcionario.salario),
  })
  const [error, setError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target
    setFormData((currentData) => ({ ...currentData, [name]: value }))
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    setIsSubmitting(true)

    try {
      const response = await fetch(`http://localhost:8080/api/v1/funcionarios/${funcionario.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, salario: Number(formData.salario) }),
      })
      const errorData = response.ok ? null : await response.json().catch(() => null)

      if (!response.ok) {
        setError(getErrorMessage(errorData))
        return
      }

      onSuccess()
    } catch {
      setError('Não foi possível conectar à API de funcionários.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mb-8 rounded-md border border-emerald-500/30 bg-slate-900/60 p-5">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <h3 className="text-lg font-bold text-white">Editar funcionário</h3>
        <button type="button" onClick={onCancel} className="text-sm text-slate-400 hover:text-white">Cancelar</button>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <label className="text-sm font-medium text-slate-300">
          Nome completo
          <input className={inputClassName} name="nome" value={formData.nome} onChange={handleChange} required />
        </label>
        <label className="text-sm font-medium text-slate-300">
          E-mail
          <input className={inputClassName} type="email" name="email" value={formData.email} onChange={handleChange} required />
        </label>
        <label className="text-sm font-medium text-slate-300">
          Telefone
          <input className={inputClassName} name="telefone" value={formData.telefone} onChange={handleChange} required />
        </label>
        <label className="text-sm font-medium text-slate-300">
          Cargo
          <input className={inputClassName} name="cargo" value={formData.cargo} onChange={handleChange} required />
        </label>
        <label className="text-sm font-medium text-slate-300">
          Salário
          <input className={inputClassName} type="number" min="1100" step="0.01" name="salario" value={formData.salario} onChange={handleChange} required />
        </label>
      </div>

      {error && <p className="mt-4 rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300" role="alert">{error}</p>}
      <button type="submit" disabled={isSubmitting} className="mt-5 rounded-md bg-emerald-500 px-4 py-2 font-semibold text-slate-950 hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-60">
        {isSubmitting ? 'Salvando...' : 'Salvar alterações'}
      </button>
    </form>
  )
}