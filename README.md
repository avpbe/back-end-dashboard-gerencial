# API - Sistema de Gerenciamento de Projetos de Engenharia

Esta é a API backend para o dashboard de gerenciamento de projetos. Desenvolvida em Python com Flask, ela fornece endpoints para operações CRUD (Criar, Ler, Atualizar, Deletar) de projetos e colaboradores.

## Tecnologias Utilizadas

- **Python 3**
- **Flask**: Micro-framework web para a criação da API.
- **Flask-OpenAPI3**: Para geração automática de documentação interativa (Swagger UI).
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Pydantic**: Para validação de dados e definição de schemas.
- **SQLite**: Banco de dados relacional leve e baseado em arquivo.
- **API RandomUser**: Serviço externo utilizado para geração e sugestão de colaboradores fictícios.

---

## Pré-requisitos

- Python 3.8 ou superior (para execução local).
- `pip` e `virtualenv` instalados (para execução local).
- **Docker** *(opcional, caso queira executar a aplicação via container)*.

---

## Como Rodar

### Opção 1: Execução Local (Sem Docker)

#### 1. Configuração do Ambiente
Clone o repositório e navegue até a pasta da API. É altamente recomendado criar um ambiente virtual.

```bash
# Navegue até a pasta da API
cd path/to/your/project/back-end-dashboard-gerencial

# Crie um ambiente virtual
python -m venv env

# Ative o ambiente virtual
# No Windows:
.\env\Scripts\activate
# No macOS/Linux:
source env/bin/activate
```

#### 2. Instalação das Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias a partir do arquivo `requirements.txt`.

```bash
(env)$ pip install -r requirements.txt
```

#### 3. Execução da API

Para iniciar o servidor de desenvolvimento, use o comando `flask run`. Na primeira vez que a API for executada, o arquivo de banco de dados `requisicoes.db` será criado automaticamente.

```bash
(env)$ flask run --host 0.0.0.0 --port 5000
```

O servidor estará rodando em `http://127.0.0.1:5000`.

### Opção 2: Execução Local (Com Docker)

Caso prefira rodar a aplicação em um container Docker, dispensando a necessidade de configurar o ambiente Python localmente:

#### 1. Construir a Imagem

Na raiz do projeto (onde está o `Dockerfile`), execute:

```bash
docker build -t api-dashboard .
```

#### 2. Iniciar o Container

Inicie o container mapeando a porta 5000:

```bash
docker run -p 5000:5000 --name api-dashboard-container api-dashboard
```

---

### Acessando a Documentação

Com a API em execução, acesse a documentação interativa do Swagger no seu navegador:

**http://127.0.0.1:5000/openapi**

Lá, você pode visualizar e testar todas as rotas disponíveis.

---

## Integração com API Externa

A API conta com uma integração com a **[RandomUser API](https://randomuser.me/)** para sugerir candidatos a colaboradores com dados complementares gerados para o contexto de engenharia:

- **Endpoint:** `GET /colaboradores/externos`
- **Parâmetros de Consulta (Query Params):**
  - `page` *(opcional, default: `1`)*: Página de resultados a consultar.
  - `results` *(opcional, default: `6`)*: Quantidade de colaboradores a retornar.
  - `nat` *(opcional, default: `br`)*: Nacionalidade dos perfis gerados.
- **Comportamento:** A rota consulta o serviço externo, filtra perfis com nomes já existentes no banco local para evitar duplicidades e associa dinamicamente cargo, disciplina e atribuição.

---

## Arquitetura do Sistema

Visão geral da comunicação e do fluxo de dados entre a Single Page Application (SPA), a API Backend e as integrações externas:

<div align="center">
  <img src="assets/arquitetura.png" alt="Fluxograma da Arquitetura do Sistema" width="800">
  <p><em>Fluxograma da arquitetura e fluxo de integração entre os componentes</em></p>
</div>
---
