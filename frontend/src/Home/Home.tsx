
import { FuncionarioForm } from '../Fornecedor/FuncionarioForm'
import { FuncionarioList } from '../Fornecedor/FuncionarioList'
import { useState } from 'react'
import { ProdutoForm } from '../Produtos/ProdutoForm'
import { ProdutoList } from '../Produtos/ProdutoList'
import { VendaForm } from '../Vendas/VendaForm'
import { VendaList } from '../Vendas/VendaList'

interface HomeProps {
  activeSection: string
}

const sectionContent: Record<string, { title: string; description: string; endpoint: string }> = {
  inicio: {
    title: 'Início',
    description: 'Selecione uma opção no menu para acessar os recursos da API.',
    endpoint: 'Painel principal',
  },
  fornecedor: {
    title: 'Funcionários',
    description: 'Consulte e gerencie os funcionários cadastrados no sistema.',
    endpoint: '/api/v1/funcionarios/',
  },
  'fornecedor-cadastrar': {
    title: 'Cadastrar funcionário',
    description: 'Adicione um novo funcionário à API de funcionários.',
    endpoint: '/api/v1/funcionarios/',
  },
  'fornecedor-listar': {
    title: 'Listar funcionários',
    description: 'Consulte e gerencie os funcionários cadastrados no sistema.',
    endpoint: '/api/v1/funcionarios/',
  },
  produtos: {
    title: 'Produtos',
    description: 'Consulte e gerencie os produtos disponíveis no mercado.',
    endpoint: '/api/v1/produtos/',
  },
  'produtos-cadastrar': { title: 'Cadastrar produto', description: 'Adicione um novo produto à API de produtos.', endpoint: '/api/v1/produtos/' },
  'produtos-listar': { title: 'Listar produtos', description: 'Consulte e gerencie os produtos cadastrados.', endpoint: '/api/v1/produtos/' },
  vendas: {
    title: 'Vendas',
    description: 'Consulte e gerencie as vendas realizadas.',
    endpoint: '/api/v1/vendas/',
  },
  'vendas-cadastrar': { title: 'Cadastrar venda', description: 'Registre uma nova venda na API de vendas.', endpoint: '/api/v1/vendas/' },
  'vendas-listar': { title: 'Listar vendas', description: 'Consulte e gerencie as vendas cadastradas.', endpoint: '/api/v1/vendas/' },
}

export function Home({ activeSection }: HomeProps) {
  const [listRefreshKey, setListRefreshKey] = useState(0)
  const content = sectionContent[activeSection] ?? sectionContent.inicio

  return (
    <main className="flex min-h-screen flex-1 justify-center bg-slate-900 p-4 text-white md:p-8">
      <section className="w-full max-w-6xl rounded-lg border border-slate-700 bg-slate-800 p-8 shadow-xl">
        <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-emerald-400">
          Área administrativa
        </p>
        <h1 className="mb-3 text-3xl font-bold text-white">{content.title}</h1>
        <p className="text-slate-300">{content.description}</p>
        {activeSection === 'fornecedor-cadastrar' ? (
          <FuncionarioForm onSuccess={() => setListRefreshKey((currentKey) => currentKey + 1)} />
        ) : activeSection === 'fornecedor-listar' ? (
          <>
            <FuncionarioList refreshKey={listRefreshKey} />
          </>
        ) : activeSection === 'produtos-cadastrar' ? (
          <ProdutoForm />
        ) : activeSection === 'produtos-listar' ? (
          <ProdutoList refreshKey={listRefreshKey} />
        ) : activeSection === 'vendas-cadastrar' ? (
          <VendaForm onSuccess={() => setListRefreshKey((currentKey) => currentKey + 1)} />
        ) : activeSection === 'vendas-listar' ? (
          <VendaList refreshKey={listRefreshKey} />
        ) : (
          <div className="mt-8 rounded-md border border-slate-700 bg-slate-900/60 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Rota da API</p>
            <code className="mt-2 block text-emerald-300">{content.endpoint}</code>
          </div>
        )}
      </section>
    </main>
  )
}