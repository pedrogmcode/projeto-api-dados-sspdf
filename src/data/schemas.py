'''
Schemas Pydantic para validação de dados
'''

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    # Status possíveis de uma tarefa
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"

class TaskPriority(str, Enum):
    # Prioridades possíveis
    BAIXA = "baixa" 
    MEDIA = "media"
    ALTA = "alta"

class TaskCreate(BaseModel):
    '''
    Schema para criar uma nova tarefa
    Usado no POST /tasks
    '''

    titulo: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Titulo da Tarefa"
    )
    
    descrivao: Optional[str] = Field(
        None,
        max_length=200,
        description="Descrição da Tarefa"
    )

    prioridade: TaskPriority = Field(
        default=TaskPriority.MEDIA,
        description="Prioridade da tarefa"
    )

    @field_validator('titulo')
    @classmethod
    def titulo_nao_vazio(cls, v: str) -> str:
        '''Valida que o título nao contém apenas espaços'''
        if not v.strip():
            raise ValueError('O título não pode estar vazio')
        return v.strip()