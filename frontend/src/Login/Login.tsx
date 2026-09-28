import React, { useState } from 'react';

// 1. Definindo a interface com os tipos dos dados do formulário
interface FormData {
    userName:string
    password:string
}

interface LoginProps {
  onLoginSuccess: () => void
}

export function Login({ onLoginSuccess }: LoginProps) {
  // 2. Estado do formulário tipado
  const [formData, setFormData] = useState<FormData>({
    userName: '',
    password: '',
  });

  const [erro, setErro] = useState<string | null>(null);

  // 3. Tipando o evento de mudança dos inputs
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  // 4. Tipando o envio do formulário
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErro(null);

    try {
      const response = await fetch(
        'http://localhost:8080/api/v1/funcionarios/auth/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            cpf: formData.userName,
            senha: formData.password,
          }),
        },
      );
      const data = await response.json();

      if (!response.ok) {
        setErro(data.detail ?? 'Erro ao realizar login');
        return;
      }

      onLoginSuccess();
    } catch {
      setErro('Não foi possível conectar ao serviço de login. Tente novamente.');
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-900 p-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md rounded-lg bg-slate-800 p-6 shadow-xl border border-slate-700"
      >
        <h2 className="mb-6 text-2xl font-bold text-white">Login</h2>

        {erro && (
          <div role="alert" className="mb-4 rounded border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-400">
            {erro}
          </div>
        )}

        <div className="mb-4">
          <label htmlFor="nome" className="mb-1 block text-sm font-medium text-slate-300">
            CPF:
          </label>
          <input
            type="text"
            id="userName"
            name="userName"
            value={formData.userName}
            onChange={handleChange}
            className="w-full rounded-md border border-slate-600 bg-slate-700 px-3.5 py-2 text-white placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            placeholder="Seu nome completo"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="password" className="mb-1 block text-sm font-medium text-slate-300">
            Senha
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="w-full rounded-md border border-slate-600 bg-slate-700 px-3.5 py-2 text-white placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            placeholder="Digite sua senha"
          />
        </div>
        <button
          type="submit"
          className="w-full rounded-md bg-indigo-600 px-4 py-2 font-semibold text-white transition hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-slate-800"
        >
          Entrar
        </button>
      </form>
    </div>
  );
}