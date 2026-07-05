from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from models import StatusProjeto
from schemas.colaborador import ColaboradorViewSchema

class ProjetoSchema(BaseModel):
    """ Define como um novo projeto a ser inserido deve ser representado """
    nome_projeto: str = "Projeto Alfa"
    disciplina: str = "Instalação"
    descricao: str = "Análise de dutos flexíveis"
    status: StatusProjeto = StatusProjeto.ABERTO
    data_inicio: datetime
    data_fim: datetime
    colaborador_id: Optional[int] = None

class ProjetoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por nome do projeto. """
    nome_projeto: str = "Projeto Alfa"

class ProjetoUpdateSchema(BaseModel):
    """ Define como um projeto pode ser atualizado. Todos os campos são opcionais. """
    nome_projeto: Optional[str] = None
    disciplina: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[StatusProjeto] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    colaborador_id: Optional[int] = None

class ProjetoViewSchema(BaseModel):
    """ Define como um projeto será retornado, incluindo o colaborador. """
    model_config = ConfigDict(from_attributes=True)

    id: int = 1
    nome_projeto: str = "Projeto Alfa"
    disciplina: str = "Instalação"
    descricao: str = "Análise de dutos flexíveis"
    status: StatusProjeto = StatusProjeto.ABERTO
    data_inicio: datetime
    data_fim: datetime
    colaborador: Optional[ColaboradorViewSchema] = None

class ListagemProjetosSchema(BaseModel):
    """ Define como uma listagem de projetos será retornada. """
    projetos: List[ProjetoViewSchema]

def apresenta_projetos(projetos: List[any]):
    """ Retorna uma representação do projeto seguindo o schema definido em ProjetoViewSchema. """
    result = []
    for proj in projetos:
        # Serializa o objeto e o converte para um dicionário JSON compatível
        result.append(ProjetoViewSchema.model_validate(proj).model_dump())
    return {"projetos": result}