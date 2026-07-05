from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote
 
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
 
from models import Session, Projeto, Colaborador, Base, engine, StatusProjeto
from schemas import (
    ProjetoSchema, ProjetoBuscaSchema, ProjetoUpdateSchema, ProjetoViewSchema, ListagemProjetosSchema, apresenta_projetos,
    ColaboradorSchema, ColaboradorBuscaSchema, ColaboradorUpdateSchema, ColaboradorDelSchema, ColaboradorViewSchema, ListagemColaboradoresSchema, apresenta_colaboradores,
    ErrorSchema
)
from flask_cors import CORS
 
info = Info(title="MVP - API de Projetos de Engenharia", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)
 
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
projeto_tag = Tag(name="Projeto", description="Adição, visualização e remoção de projetos à base")
colaborador_tag = Tag(name="Colaborador", description="Adição, visualização e remoção de colaboradores da base")
 
 
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela de documentação swagger.
    """
    return redirect('/openapi')
 
# Rota para adicionar um novo projeto
@app.post('/projeto', tags=[projeto_tag],
          responses={"200": ProjetoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_projeto(body: ProjetoSchema):
    """Adiciona um novo Projeto à base de dados
 
    Retorna uma representação do projeto inserido.
    """
    session = Session()
    colaborador = None
    if body.colaborador_id:
        colaborador = session.query(Colaborador).filter(Colaborador.id == body.colaborador_id).first()
        if not colaborador:
            return {"message": "Colaborador não encontrado."}, 404

    projeto = Projeto(
        nome_projeto=body.nome_projeto,
        disciplina=body.disciplina,
        descricao=body.descricao,
        status=body.status,
        data_inicio=body.data_inicio,
        data_fim=body.data_fim,
        colaborador_id=body.colaborador_id
    )
 
    try:
        session.add(projeto)
        session.commit()
        # Serializa o objeto para o schema de visualização e o converte para um dicionário
        projeto_apresentado = ProjetoViewSchema.model_validate(projeto)
        return projeto_apresentado.model_dump(), 200
 
    except IntegrityError as e:
        session.rollback()
        error_msg = "Projeto com o mesmo nome já salvo na base."
        return {"message": error_msg}, 409
 
    except Exception as e:
        session.rollback()
        error_msg = "Não foi possível salvar novo projeto."
        return {"message": error_msg}, 400
    finally:
        session.close()

# Rota para buscar todos os projetos
@app.get('/projetos', tags=[projeto_tag],
         responses={"200": ListagemProjetosSchema, "404": ErrorSchema})
def get_projetos():
    """Faz a busca por todos os Projetos cadastrados
    """
    session = Session()
    try:
        # Realiza o join para carregar os dados do colaborador junto com o projeto (eager loading)
        # para evitar o DetachedInstanceError ao acessar o relacionamento após fechar a sessão.
        projetos = session.query(Projeto).options(joinedload(Projeto.colaborador)).all()
        
        if not projetos:
            return {"projetos": []}, 200
        else:
            return apresenta_projetos(projetos), 200
    finally:
        session.close()

# Rota para buscar projetos por nome
@app.get('/projetos/busca', tags=[projeto_tag],
         responses={"200": ListagemProjetosSchema, "404": ErrorSchema})
def search_projetos(query: ProjetoBuscaSchema):
    """Faz a busca por Projetos a partir de um termo pesquisado no nome.
    """
    termo_busca = query.nome_projeto
    session = Session()
    try:
        # Filtra projetos usando 'ilike' para busca case-insensitive e parcial
        query_result = session.query(Projeto).options(joinedload(Projeto.colaborador)).filter(Projeto.nome_projeto.ilike(f'%{termo_busca}%'))
        projetos = query_result.all()
        
        return apresenta_projetos(projetos), 200
    finally:
        session.close()


# Rota para atualizar um projeto
@app.put('/projeto', tags=[projeto_tag],
         responses={"200": ProjetoViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_projeto(query: ProjetoBuscaSchema, body: ProjetoUpdateSchema):
    """Atualiza um Projeto existente a partir do nome do projeto informado.
    """
    session = Session()
    # Carrega o projeto e o colaborador relacionado para evitar DetachedInstanceError
    projeto = session.query(Projeto).options(joinedload(Projeto.colaborador)).filter(Projeto.nome_projeto == query.nome_projeto).first()

    if not projeto:
        session.close()
        return {"message": "Projeto não encontrado."}, 404

    # Atualiza os campos do projeto se eles foram fornecidos no corpo da requisição
    # O método `dict(exclude_unset=True)` do Pydantic é perfeito para isso
    update_data = body.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(projeto, key, value)

    try:
        session.commit()
        # Retorna a representação atualizada do projeto
        return ProjetoViewSchema.model_validate(projeto).model_dump(), 200
    except IntegrityError as e:
        session.rollback()
        # Se o novo nome do projeto já existir
        return {"message": "Já existe um projeto com este novo nome."}, 409
    except Exception as e:
        session.rollback()
        error_msg = "Não foi possível atualizar o projeto."
        return {"message": error_msg}, 400
    finally:
        session.close()


# Rota para deletar um projeto
@app.delete('/projeto', tags=[projeto_tag],
            responses={"200": ProjetoViewSchema, "404": ErrorSchema})
def del_projeto(query: ProjetoBuscaSchema):
    """Deleta um Projeto a partir do nome do projeto informado
    """
    nome_projeto = unquote(unquote(query.nome_projeto))
    session = Session()
    count = session.query(Projeto).filter(Projeto.nome_projeto == nome_projeto).delete()
    session.commit()
    session.close()
    
    if count:
        return {"message": "Projeto removido", "id": nome_projeto}
    else:
        error_msg = "Projeto não encontrado na base."
        return {"message": error_msg}, 404
 

# ======================== ROTAS DE COLABORADOR ========================

@app.post('/colaborador', tags=[colaborador_tag],
          responses={"200": ColaboradorSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_colaborador(body: ColaboradorSchema):
    """Adiciona um novo Colaborador à base de dados
    """
    colaborador = Colaborador(
        nome=body.nome,
        cargo=body.cargo,
        disciplina=body.disciplina,
        atribuicao=body.atribuicao
    )

    try:
        session = Session()
        session.add(colaborador)
        session.commit()
        return apresenta_colaboradores([colaborador])['colaboradores'][0], 200

    except IntegrityError:
        session.rollback()
        error_msg = "Colaborador com o mesmo nome já salvo na base."
        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()
        error_msg = "Não foi possível salvar novo colaborador."
        return {"message": str(e)}, 400
    finally:
        session.close()

@app.get('/colaboradores', tags=[colaborador_tag],
         responses={"200": ListagemColaboradoresSchema, "404": ErrorSchema})
def get_colaboradores():
    """Faz a busca por todos os Colaboradores cadastrados
    """
    session = Session()
    colaboradores = session.query(Colaborador).all()
    session.close()

    if not colaboradores:
        return {"colaboradores": []}, 200
    else:
        return apresenta_colaboradores(colaboradores), 200

@app.put('/colaborador', tags=[colaborador_tag],
            responses={"200": ColaboradorViewSchema, "404": ErrorSchema, "400": ErrorSchema, "409": ErrorSchema})
def update_colaborador(query: ColaboradorBuscaSchema, body: ColaboradorUpdateSchema):
    """Atualiza um Colaborador existente a partir do nome informado.
    """
    session = Session()
    colaborador = session.query(Colaborador).filter(Colaborador.nome == query.nome).first()

    if not colaborador:
        session.close()
        return {"message": "Colaborador não encontrado."}, 404

    # Atualiza os campos do colaborador se eles foram fornecidos no corpo da requisição
    update_data = body.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(colaborador, key, value)

    try:
        session.commit()
        # Retorna a representação atualizada do colaborador
        return ColaboradorViewSchema.model_validate(colaborador).model_dump(), 200
    except IntegrityError:
        session.rollback()
        return {"message": "Já existe um colaborador com este novo nome."}, 409
    except Exception as e:
        session.rollback()
        error_msg = "Não foi possível atualizar o colaborador."
        return {"message": error_msg}, 400
    finally:
        session.close()


@app.delete('/colaborador', tags=[colaborador_tag],
            responses={"200": ColaboradorDelSchema, "404": ErrorSchema, "400": ErrorSchema})
def del_colaborador(query: ColaboradorBuscaSchema):
    """Deleta um Colaborador a partir do nome informado
    """
    nome_colaborador = unquote(unquote(query.nome))
    session = Session()

    # Verifica se o colaborador está alocado em algum projeto
    colaborador = session.query(Colaborador).filter(Colaborador.nome == nome_colaborador).first()
    if colaborador and colaborador.projetos:
        session.close()
        return {"message": "Não é possível remover. Colaborador está alocado em um ou mais projetos."}, 400

    count = session.query(Colaborador).filter(Colaborador.nome == nome_colaborador).delete()
    session.commit()
    session.close()

    if count:
        return {"message": "Colaborador removido", "nome": nome_colaborador}, 200
    else:
        error_msg = "Colaborador não encontrado na base."
        return {"message": error_msg}, 404


if __name__ == '__main__':
    # Cria o banco de dados e as tabelas, se não existirem
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5000)
