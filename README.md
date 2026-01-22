# Clarke Energia - Simulador de Economia

Aplicação web para simulação de economia com fornecedores de energia renovável (GD e Mercado Livre).

## 🚀 Tecnologias

- **Frontend**: React + Vite + Apollo Client
- **Backend**: Python FastAPI + GraphQL (Strawberry)
- **Containerização**: Docker + Docker Compose

## 📋 Pré-requisitos

- Docker Desktop
- Git

## 🐳 Rodando com Docker (Recomendado)
```bash
# Clone o repositório
git clone <seu-repositorio>
cd Clarke

# Inicie os containers
docker compose up --build

# Acesse:
# Frontend: http://localhost:5173
# Backend GraphQL: http://localhost:8000/graphql
```

## 💻 Rodando sem Docker

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🎯 Funcionalidades

- ✅ Seleção de estado (UF)
- ✅ Cálculo de economia por consumo (kWh)
- ✅ Comparação entre fornecedores
- ✅ Visualização de soluções (GD e Mercado Livre)
- ✅ API GraphQL completa

## 📦 Estrutura do Projeto
```
Clarke/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schema.py
│   │   └── data.py
│   ├── Dockerfile
│   ├── .dockerignore
│   └── requirements.txt
├── frontend/
|   |__ public
|   |   └── favicon.png
|   |   
│   ├── src/
│   │   ├── graphql/
│   │   │   └── queries.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── Index.css
│   │   ├── apolloClient.js
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── .dockerignore
│   └── package.json
└── docker-compose.yml
```

## 🧪 Diferenciais Implementados

- ✅ **GraphQL** (Apollo Client + Strawberry)
- ✅ **Docker** (Dockerfiles + Docker Compose)

## 👥 Autora

Thaysa Rafaele - Desafio Técnico Clarke Energia 2026