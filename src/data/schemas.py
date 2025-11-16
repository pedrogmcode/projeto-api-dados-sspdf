# Arquivo: src/data/schemas.py
# Esquemas Pydantic para validação e serialização de dados
# Autor: Casimiro
# Data: 2024-06-15

from pydantic import BaseModel, Field
from typing import Optional, List 

# Esquema de INPUT (O que o usuário envia)
class OcorrenciasRequest(BaseModel):
    Mes: int = Field(..., ge=1, le=12, description="Mês da ocorrência (1-12)")
    Ano: int = Field(..., ge=2000, le=2100, description="Ano da ocorrência (2000-2100)")
    class Config:json_schema_extra  = {"example": {"Mes": 6, "Ano": 2024}}

# Esquema de OUTPUT (O que a API retorna para CADA ocorrência)
# Os nomes dos campos devem refletir suas colunas do CSV após padronização, 
# mas usando a notação CaseSensitive do Pydantic (ex: Natureza, Mes)
class OcorrenciasResponse(BaseModel):
    id: int = Field(..., description="Identificador único da ocorrência")
    Natureza: str = Field(..., description="Natureza da ocorrência")
    Mes: int = Field(..., ge=1, le=12, description="Mês da ocorrência (1-12)")
    Ano: int = Field(..., ge=2000, le=2100, description="Ano da ocorrência (2000-2100)")
    class Config:json_schema_extra  = {"example": {"id": 1, "Natureza": "Roubo", "Mes": 6, "Ano": 2024}}
    
# Esquema de health check (permanece igual)
class HealthCheck(BaseModel):
    status: str = Field(Optional, description="Status da API")
    service: str = Field(Optional, description="Nome do serviço")
    version: str = Field(Optional, description="Versão do serviço")