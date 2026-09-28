import { useState } from 'react'
import type { FormEvent } from 'react'

interface FuncionarioFormData {
  nome: string
  cpf: string
  email: string
  telefone: string
  data_nascimento: string
  cargo: string
  salario: string
  senha: string
  data_contratacao: string
}

const initialFormData: FuncionarioFormData = {
  nome: '',
  cpf: '',
  email: '',
  telefone: '',
  data_nascimento: '',
  cargo: '',
  salario: '',
  senha: '',
  data_contratacao: '',
}

const inputClassName = 'w-full rounded-md border border-slate-600 bg-slate-700 px-3 py-2 text-white placeholder-slate-400 focus:border-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400'

function getErrorMessage(errorData: { detail?: string | { msg?: string }[] } | null) {
  if (Array.isArray(errorData?.detail)) {
    return errorData.detail.map((error) => error.msg ?? 'Valor inválido').join('; ')
  }

  return errorData?.detail ?? 'Não foi possível cadastrar o funcionário.'
}

interface FuncionarioFormProps {
  onSuccess?: () => void
}

export function FuncionarioForm({ onSuccess }: FuncionarioFormProps) {
  const [formData, setFormData] = useState(initialFormData)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target
    setFormData((currentData) => ({ ...currentData, [name]: value }))
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    setSuccess(null)
    setIsSubmitting(true)

    try {
      const response = await fetch('http://localhost:8080/api/v1/funcionarios/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...formData,
          salario: Number(formData.salario),
        }),
      })
      const errorData = response.ok ? null : await response.json().catch(() => null)

      if (!response.ok) {
        setError(getErrorMessage(errorData))
        return
      }

      setFormData(initialFormData)
      setSuccess('Funcionário cadastrado com sucesso.')
      onSuccess?.()
    } catch {
      setError('Não foi possível conectar à API de funcionários.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mt-8 grid gap-5 md:grid-cols-2">
      <label className="text-sm font-medium text-slate-300">
        Nome completo
        <input className={inputClassName} name="nome" value={formData.nome} onChange={handleChange} required />
      </label>

      <label className="text-sm font-medium text-slate-300">
        CPF
        <input className={inputClassName} name="cpf" value={formData.cpf} onChange={handleChange} placeholder="00000000000" required />
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
        Data de nascimento
        <input className={inputClassName} type="date" name="data_nascimento" value={formData.data_nascimento} onChange={handleChange} required />
      </label>

      <label className="text-sm font-medium text-slate-300">
        Data de contratação
        <input className={inputClassName} type="date" name="data_contratacao" value={formData.data_contratacao} onChange={handleChange} required />
      </label>

      <label className="text-sm font-medium text-slate-300">
        Cargo
        <input className={inputClassName} name="cargo" value={formData.cargo} onChange={handleChange} required />
      </label>

      <label className="text-sm font-medium text-slate-300">
        Salário
        <input className={inputClassName} type="number" min="1100" step="0.01" name="salario" value={formData.salario} onChange={handleChange} required />
      </label>

      <label className="text-sm font-medium text-slate-300 md:col-span-2">
        Senha
        <input className={inputClassName} type="password" minLength={8} name="senha" value={formData.senha} onChange={handleChange} required />
      </label>

      {error && <p className="md:col-span-2 rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300" role="alert">{error}</p>}
      {success && <p className="md:col-span-2 rounded-md border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-300" role="status">{success}</p>}

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-md bg-emerald-500 px-4 py-2 font-semibold text-slate-950 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-60 md:col-span-2"
      >
        {isSubmitting ? 'Cadastrando...' : 'Cadastrar funcionário'}
      </button>
    </form>
  )
}