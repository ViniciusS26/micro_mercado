#  Bem Vindo ao Projeto

Aqui será construido durante 3 meses um microsservice para resolver o problema de um mercado.



Primeiro uma breve introdução sobre microsserviços

<p>A arquitetura de microsserviço, também conhecida como microsserviços, é o método arquitetônico que depende da série de serviços implantáveis com independência. Esses serviços têm sua própria lógica de negócios e banco de dados com objetivo específico. A atualização, o teste, a implementação e a escalabilidade ocorrem em cada serviço. Os microsserviços dissociam os principais problemas específicos dos domínios de negócios em bases de código independentes separadas. Os microsserviços não reduzem a complexidade, mas tornam qualquer complexidade visível e mais gerenciável, separando as tarefas em processos menores que funcionam independentes uns dos outros e contribuem para o todo.<p>

A adoção do microsserviços muitas vezes anda de mãos dadas com o DevOps, pois eles são base para práticas de entrega contínua que permitem que as equipes se adaptem com rapidez aos requisitos do usuário.


## E com ta organizado os requisitos desse projeto?

Levando em consideração o conceito de microsserviços estruturamos o projeto da seguinte forma:



![Micro_servico](/imgs/estrutura_micro_service.png)


## E qual tecnologia vamos usar?

Todo o projeto será desenvolvido usando as tencologias:


Frontend:<p>
   - VueJS + Vuetfy<p>


Backend:<p>
  -  Python <p>
  -  FastAPI <p>
  - Postgresql <p>

## Como deve ficar a estrutura de pastas do projeto
### Estrutura do Projeto - Sistema SGM

Este projeto utiliza uma arquitetura de microsserviços e a abordagem de monorepo para organizar o código.

```plaintext
/micro-mercado/
├── .gitignore
├── docker-compose.yml         # Orquestra todos os serviços para o ambiente de desenvolvimento
├── README.md
│
├── 📂 api-gateway/            # Ponto de entrada da API (FastAPI) que se comunica com Front-end
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── 📂 frontend/                   # Aplicação do cliente (Vue.js)
│   ├── public/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
│
└── 📂 services/                   # Contêiner para todos os microsserviços de negócio
    │
    ├── 📂 ms-funcionarios/
    │   ├── app/
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── 📂 ms-fornecedores/
    │   ├── app/
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── 📂 ms-produtos/
    │   ├── app/
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── 📂 ms-relatorios/
    │   ├── app/
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    └── 📂 ms-vendas/
        ├── app/
        ├── Dockerfile
        └── requirements.txt
```

### Exemplo de Estrutura de cada pasta
```
# Pasta que fica a api gateway que comunica com cada serviço

/api-gateway/
├── 🐳 Dockerfile                 # Define a imagem Docker para o gateway
├── 📄 requirements.txt           # Dependências Python (fastapi, uvicorn, httpx)
└── 📂 app/
    ├── 📄 __init__.py
    ├── 📄 main.py                 # Ponto de entrada da aplicação FastAPI
    ├── 📂 core/
    │   └── 📄 config.py           # Configurações (URLs dos outros microsserviços)
    └── 📂 routers/
        ├── 📄 funcionarios_router.py # Roteia /api/funcionarios para o ms-funcionarios
        ├── 📄 produtos_router.py   # Roteia /api/produtos para o ms-produtos
        └── ... (etc.)
```
### Exemplo de como deve ficar origanizado os microsserviços

```
/services/ms-funcionarios/
├── 🐳 Dockerfile                 # Define a imagem Docker específica para este serviço
├── 📄 requirements.txt           # fastapi, uvicorn, sqlalchemy, psycopg2-binary
└── 📂 app/
    ├── 📄 __init__.py
    ├── 📄 main.py                 # Ponto de entrada da aplicação FastAPI do serviço
    ├── 📂 api/
    │   └── 📄 endpoints.py        # Define os endpoints (/funcionarios, /funcionarios/{id})
    ├── 📂 core/
    │   └── 📄 config.py           # Configurações (ex: string de conexão do DB)
    ├── 📂 crud/                    # Lógica de acesso ao banco (Create, Read, Update, Delete)
    │   └── 📄 funcionario_crud.py
    ├── 📂 db/
    │   └── 📄 session.py          # Gerenciamento da sessão com o PostgreSQL
    ├── 📂 models/
    │   └── 📄 funcionario_model.py # Modelo da tabela (SQLAlchemy ORM)
    └── 📂 schemas/
        └── 📄 funcionario_schema.py # Esquemas Pydantic para validação de dados (entrada/saída)

```

### Exemplo de pasta do frontend

``` 
/frontend/
├── 🐳 Dockerfile         # Define a imagem Docker (geralmente com Nginx) para servir os arquivos
├── 📄 package.json
├── 📄 vite.config.js (ou vue.config.js)
├── 📂 public/
└── 📂 src/
    ├── 📂 assets/
    ├── 📂 components/
    ├── 📂 views/
    ├── 📂 services/
    │   └── 📄 api.js              # Centraliza as chamadas à API (axios, fetch)
    ├── 📄 App.vue
    └── 📄 main.js
```
## Quem são os  contribuidores do projeto?

<img src="https://github.com/aleffericlys.png" width="60" height="60" style="border-radius: 50%;" >AlefF Ericlys[GitHub:](https://github.com/aleffericlys)

<img src="https://github.com/Vinicius02612.png" width="60" height="60" style="border-radius: 50%;">Vinicius Nunes[GitHub:](https://github.com/Vinicius02612)

<img src="https://github.com/carlosvale03.png" width="60" height="60" style="border-radius: 50%;">Carlos Henrique[GitHub:](https://github.com/carlosvale03)