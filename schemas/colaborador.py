from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from models import AtribuicaoColaborador, CargoColaborador, Colaborador

class ColaboradorSchema(BaseModel):
    """ Define como um novo colaborador a ser inserido deve ser representado """
    nome: str = "João da Silva"
    cargo: CargoColaborador = CargoColaborador.SENIOR
    disciplina: str = "Estruturas"
    atribuicao: AtribuicaoColaborador = AtribuicaoColaborador.ELABORADOR

class ColaboradorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por nome. """
    nome: str = "João da Silva"

class ColaboradorUpdateSchema(BaseModel):
    """ Define como um colaborador pode ser atualizado. Todos os campos são opcionais. """
    nome: Optional[str] = None
    cargo: Optional[CargoColaborador] = None
    disciplina: Optional[str] = None
    atribuicao: Optional[AtribuicaoColaborador] = None

class ColaboradorViewSchema(BaseModel):
    """ Define como um colaborador será retornado """
    model_config = ConfigDict(from_attributes=True)

    id: int = 1
    nome: str = "João da Silva"
    cargo: CargoColaborador = CargoColaborador.SENIOR
    disciplina: str = "Estruturas"
    atribuicao: AtribuicaoColaborador = AtribuicaoColaborador.ELABORADOR

class ListagemColaboradoresSchema(BaseModel):
    """ Define como uma listagem de colaboradores será retornada. """
    colaboradores: List[ColaboradorViewSchema]

class ColaboradorDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str

def apresenta_colaboradores(colaboradores: List[Colaborador]):
    """ Retorna uma representação do colaborador seguindo o schema definido em
        ListagemColaboradoresSchema.
    """
    result = []
    for colab in colaboradores:
        # Serializa o objeto e o converte para um dicionário JSON compatível
        result.append(ColaboradorViewSchema.model_validate(colab).model_dump())
    return {"colaboradores": result}