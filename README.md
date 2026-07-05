# API - Sistema de Gerenciamento de Projetos de Engenharia

Esta é a API backend para o dashboard de gerenciamento de projetos. Desenvolvida em Python com Flask, ela fornece endpoints para operações CRUD (Criar, Ler, Atualizar, Deletar) de projetos e colaboradores.

## Tecnologias Utilizadas

- **Python 3**
- **Flask**: Micro-framework web para a criação da API.
- **Flask-OpenAPI3**: Para geração automática de documentação interativa (Swagger UI).
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Pydantic**: Para validação de dados e definição de schemas.
- **SQLite**: Banco de dados relacional leve e baseado em arquivo.

---

## Instruções de Instalação e Execução

### Pré-requisitos

- Python 3.8 ou superior.
- `pip` e `virtualenv` instalados.

### 1. Configuração do Ambiente

Clone o repositório e navegue até a pasta da API. É altamente recomendado criar um ambiente virtual.

```bash
# Navegue até a pasta da API
cd path/to/your/project/engineer_requisitions/api

# Crie um ambiente virtual
python -m venv env

# Ative o ambiente virtual
# No Windows:
.\env\Scripts\activate
# No macOS/Linux:
source env/bin/activate
```

### 2. Instalação das Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias a partir do arquivo `requirements.txt`.

```bash
(env)$ pip install -r requirements.txt
```

### 3. Execução da API

Para iniciar o servidor de desenvolvimento, use o comando `flask run`. Na primeira vez que a API for executada, o arquivo de banco de dados `requisicoes.db` será criado automaticamente.

```bash
(env)$ flask run --host 0.0.0.0 --port 5000
```

O servidor estará rodando em `http://127.0.0.1:5000`.

### 4. Acessando a Documentação

Com a API em execução, acesse a documentação interativa do Swagger no seu navegador:

**http://127.0.0.1:5000/openapi**

Lá, você pode visualizar e testar todas as rotas disponíveis.