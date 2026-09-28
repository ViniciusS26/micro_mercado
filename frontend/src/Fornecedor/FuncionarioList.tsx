import { useEffect, useState } from 'react'
import { FuncionarioEditForm } from './FuncionarioEditForm'

export interface Funcionario {
  id: number
  nome: string
  cpf: string
  email: string
  telefone: string
  cargo: string
  salario: number
  data_contratacao: string
}

interface FuncionarioListProps {
  refreshKey: number
}

function formatDate(date: string) {
  return new Date(`${date}T00:00:00`).toLocaleDateString('pt-BR')
}

export function FuncionarioList({ refreshKey }: FuncionarioListProps) {
  const [funcionarios, setFuncionarios] = useState<Funcionario[]>([])
  const [editingFuncionario, setEditingFuncionario] = useState<Funcionario | null>(null)
  const [localRefreshKey, setLocalRefreshKey] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<number | null>(null)

  useEffect(() => {
    let isCurrent = true

    const loadFuncionarios = async () => {
      setIsLoading(true)
      setError(null)

      try {
        const response = await fetch('http://localhost:8080/api/v1/funcionarios/')
        const data = await response.json().catch(() => null)

        if (!response.ok) {
          throw new Error(data?.detail ?? 'Não foi possível carregar os funcionários.')
        }

        if (isCurrent) {
          setFuncionarios(data)
        }
      } catch (requestError) {
        if (isCurrent) {
          setError(requestError instanceof Error ? requestError.message : 'Erro ao carregar os funcionários.')
        }
      } finally {
        if (isCurrent) {
          setIsLoading(false)
        }
      }
    }

    loadFuncionarios()

    return () => {
      isCurrent = false
    }
  }, [refreshKey, localRefreshKey])

  const handleDelete = async (funcionario: Funcionario) => {
    if (!window.confirm(`Excluir o funcionário ${funcionario.nome}?`)) {
      return
    }

    setError(null)
    setDeletingId(funcionario.id)

    try {
      const response = await fetch(`http://localhost:8080/api/v1/funcionarios/${funcionario.id}`, { method: 'DELETE' })
      const data = response.ok ? null : await response.json().catch(() => null)

      if (!response.ok) {
        throw new Error(data?.detail ?? 'Não foi possível excluir o funcionário.')
      }

      setEditingFuncionario(null)
      setLocalRefreshKey((currentKey) => currentKey + 1)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'Erro ao excluir o funcionário.')
    } finally {
      setDeletingId(null)
    }
  }

  return (
    <section className="mt-10 border-t border-slate-700 pt-8" aria-labelledby="funcionarios-title">
      <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 id="funcionarios-title" className="text-xl font-bold text-white">Funcionários cadastrados</h2>
          <p className="mt-1 text-sm text-slate-400">Dados retornados pela API de funcionários.</p>
        </div>
        {!isLoading && <span className="text-sm text-slate-400">{funcionarios.length} cadastro(s)</span>}
      </div>

      {editingFuncionario && (
        <FuncionarioEditForm
          funcionario={editingFuncionario}
          onCancel={() => setEditingFuncionario(null)}
          onSuccess={() => {
            setEditingFuncionario(null)
            setLocalRefreshKey((currentKey) => currentKey + 1)
          }}
        />
      )}

      {isLoading && <p className="text-slate-300">Carregando funcionários...</p>}
      {error && <p className="rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300" role="alert">{error}</p>}
      {!isLoading && !error && funcionarios.length === 0 && (
        <p className="rounded-md border border-slate-700 bg-slate-900/60 p-4 text-slate-300">Nenhum funcionário cadastrado.</p>
      )}

      {!isLoading && !error && funcionarios.length > 0 && (
        <div className="overflow-x-auto rounded-md border border-slate-700">
          <table className="min-w-full divide-y divide-slate-700 text-left text-sm">
            <thead className="bg-slate-900/80 text-xs uppercase tracking-wide text-slate-400">
              <tr>
                <th className="px-4 py-3">Nome</th>
                <th className="px-4 py-3">CPF</th>
                <th className="px-4 py-3">E-mail</th>
                <th className="px-4 py-3">Cargo</th>
                <th className="px-4 py-3">Salário</th>
                <th className="px-4 py-3">Contratação</th>
                <th className="px-4 py-3">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700 bg-slate-800 text-slate-200">
              {funcionarios.map((funcionario) => (
                <tr key={funcionario.id} className="hover:bg-slate-700/50">
                  <td className="whitespace-nowrap px-4 py-3 font-medium">{funcionario.nome}</td>
                  <td className="whitespace-nowrap px-4 py-3">{funcionario.cpf}</td>
                  <td className="px-4 py-3">{funcionario.email}</td>
                  <td className="whitespace-nowrap px-4 py-3">{funcionario.cargo}</td>
                  <td className="whitespace-nowrap px-4 py-3">{funcionario.salario.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}</td>
                  <td className="whitespace-nowrap px-4 py-3">{formatDate(funcionario.data_contratacao)}</td>
                  <td className="whitespace-nowrap px-4 py-3">
                    <div className="flex gap-2">
                      <button type="button" onClick={() => setEditingFuncionario(funcionario)} className="rounded-md bg-slate-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-slate-500">
                        Editar
                      </button>
                      <button type="button" onClick={() => handleDelete(funcionario)} disabled={deletingId === funcionario.id} className="rounded-md bg-red-500/80 px-3 py-1.5 text-xs font-semibold text-white hover:bg-red-500 disabled:cursor-not-allowed disabled:opacity-60">
                        {deletingId === funcionario.id ? 'Excluindo...' : 'Excluir'}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}