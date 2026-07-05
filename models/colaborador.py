from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
import enum
from models import Base

# Lista para Cargo
class CargoColaborador(str, enum.Enum):
    JUNIOR = "Engenheiro Junior"
    PLENO = "Engenheiro Pleno"
    SENIOR = "Engenheiro Senior"

# Lista para Atribuição do Colaborador
class AtribuicaoColaborador(str, enum.Enum):
    ELABORADOR = "Elaborador"
    REVISOR = "Revisor"
    APROVADOR = "Aprovador"

class Colaborador(Base):
    __tablename__ = 'colaborador'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)
    cargo = Column(SQLAlchemyEnum(CargoColaborador), nullable=False)
    disciplina = Column(String(100))
    atribuicao = Column(SQLAlchemyEnum(AtribuicaoColaborador), nullable=False)

    # Relacionamento com Projeto
    projetos = relationship("Projeto", back_populates="colaborador")