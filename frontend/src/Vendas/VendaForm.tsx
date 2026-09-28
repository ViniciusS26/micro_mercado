import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'

const inputClassName = 'w-full rounded-md border border-slate-600 bg-slate-700 px-3 py-2 text-white placeholder-slate-400 focus:border-emerald-400 focus:outline-none focus:ring-1 focus:ring-emerald-400'

interface FuncionarioOption {
  id: number
  nome: string
  cpf: string
  cargo: string
}

export function VendaForm({ onSuccess }: { onSuccess?: () => void }) {
  const [tituloProduto, setTituloProduto] = useState('')
  const [idFuncionario, setIdFuncionario] = useState('')
  const [funcionarios, setFuncionarios] = useState<FuncionarioOption[]>([])
  const [isLoadingFuncionarios, setIsLoadingFuncionarios] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    const loadFuncionarios = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/v1/funcionarios/')
        const data = await response.json().catch(() => null)

        if (!response.ok) {
          throw new Error(data?.detail ?? 'Não foi possível carregar os funcionários.')
        }

        setFuncionarios(data)
      } catch (requestError) {
        setError(requestError instanceof Error ? requestError.message : 'Erro ao carregar os funcionários.')
      } finally {
        setIsLoadingFuncionarios(false)
      }
    }

    loadFuncionarios()
  }, [])

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault(); setError(null); setSuccess(null); setIsSubmitting(true)
    try {
      const params = new URLSearchParams({ titulo_produto: tituloProduto, id_funcionario: idFuncionario })
      const response = await fetch(`http://localhost:8080/api/v1/vendas/?${params}`, { method: 'POST' })
      const data = response.ok ? null : await response.json().catch(() => null)
      if (!response.ok) { setError(data?.detail ?? 'Não foi possível cadastrar a venda.'); return }
      setTituloProduto(''); setIdFuncionario(''); setSuccess('Venda cadastrada com sucesso.'); onSuccess?.()
    } catch { setError('Não foi possível conectar à API de vendas.') } finally { setIsSubmitting(false) }
  }
  return (
    <form onSubmit={handleSubmit} className="mt-8 grid gap-5 md:max-w-2xl">
      <label className="text-sm font-medium text-slate-300">
        Título do produto
        <input className={inputClassName} value={tituloProduto} 
        onChange={(event) => setTituloProduto(event.target.value)} required />
      </label>
      <label className="text-sm font-medium text-slate-300">
        Funcionário vendedor
        <select
          className={inputClassName}
          value={idFuncionario}
          onChange={(event) => setIdFuncionario(event.target.value)}
          disabled={isLoadingFuncionarios || funcionarios.length === 0}
          required
        >
          <option value="">
            {isLoadingFuncionarios ? 'Carregando funcionários...' : 'Selecione um funcionário'}
          </option>
          {funcionarios.map((funcionario) => (
            <option key={funcionario.id} value={funcionario.id}>
              {funcionario.nome} - {funcionario.cargo} ({funcionario.cpf})
            </option>
          ))}
        </select>
      </label>
      {error && <p className="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300" role="alert">{error}</p>}
      {success && <p className="rounded-md border border-emerald-500/30 bg-emerald-500/10 p-3 text-sm text-emerald-300" role="status">{success}</p>}
      <button type="submit" disabled={isSubmitting || isLoadingFuncionarios || funcionarios.length === 0} className="rounded-md bg-emerald-500 px-4 py-2 font-semibold text-slate-950 hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-60">
        {isSubmitting ? 'Cadastrando...' : 'Cadastrar venda'}
      </button>
    </form>
  )
}