from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from models import Base

# Lista para Status do Projeto
class StatusProjeto(str, enum.Enum):
    ABERTO = "Aberto"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"

class Projeto(Base):
    __tablename__ = 'projeto'

    id = Column(Integer, primary_key=True)
    nome_projeto = Column(String(100), unique=True, nullable=False)
    disciplina = Column(String(100))
    descricao = Column(String(500))
    status = Column(SQLAlchemyEnum(StatusProjeto), nullable=False, default=StatusProjeto.ABERTO)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())

    # Chave estrangeira para o colaborador
    colaborador_id = Column(Integer, ForeignKey('colaborador.id'), nullable=True)
    colaborador = relationship("Colaborador", back_populates="projetos")

    def __init__(self, nome_projeto, disciplina, descricao, status, data_inicio, data_fim, colaborador_id=None):
        self.nome_projeto = nome_projeto
        self.disciplina = disciplina
        self.descricao = descricao
        self.status = status
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.colaborador_id = colaborador_id