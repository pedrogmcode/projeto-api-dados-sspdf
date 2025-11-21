# Arquivo: src/data/schemas.py
# Esquemas Pydantic para validação e serialização de dados
# Autor: Casimiro
# Data: 2024-06-15

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from typing import List
from enum import Enum

# --- CLASSE HEALTH CHECK ---
class HealthCheck(BaseModel):
    status: str = Field(Optional, description="Status da API")
    service: str = Field(Optional, description="Nome do serviço")
    version: str = Field(Optional, description="Versão do serviço")
    class Config:json_schema_extra  = {"example": {"status": "ok", "service": "OcorrenciasAPI", "version": "1.0.0"}}

# Esquema de INPUT (O que o usuário envia)
class OcorrenciasRequest(BaseModel):
    id_ra: int = Field(..., ge=1, le=33, description="Identificador único da Região Administrativa (RA)")
    cod_natureza: int = Field(..., ge=1, le=32, description="Código da Natureza da ocorrência")
    quantidade: int = Field(..., ge=0, description="Quantidade de ocorrências")
    mes: int = Field(..., ge=1, le=12, description="Mês da ocorrência (1-12)")
    ano: int = Field(..., ge=2000, le=2100, description="Ano da ocorrência (2000-2100)")
    class Config:json_schema_extra  = {"example": {"id_ra": 1, "cod_natureza": 1, "quantidade": 10, "mes": 6, "ano": 2024}}

'''
# --- VERSÃO ANTERIOR SEM ENUMERAÇÃO --- ALTERADO POR CASIMIRO EM 17-11-2025
# Esquema de OUTPUT (O que a API retorna para CADA ocorrência)
# Os nomes dos campos devem refletir suas colunas do CSV após padronização,
# mas usando a notação CaseSensitive do Pydantic (ex: Natureza, Mes)
class OcorrenciasResponse(BaseModel):
    id: int = Field(..., description="Identificador único da ocorrência")
    Natureza: str = Field(..., description="Natureza da ocorrência")
    Mes: int = Field(..., ge=1, le=12, description="Mês da ocorrência (1-12)")
    Ano: int = Field(..., ge=2000, le=2100, description="Ano da ocorrência (2000-2100)")
    Quantidade: int = Field(..., description="Quantidade de ocorrências")
    class Config: json_schema_extra  = {"example": {"id": 1, "Natureza": "Roubo", "Mes": 6, "Ano": 2024, "Quantidade": 10}}
'''
# --- CLASSE ENUMERADA (Valores Fixos) ---
class NaturezaOcorrencia(str, Enum):
    HOMICIDIO = "HOMICIDIO"
    FEMINICIDIO = "FEMINICIDIO"
    LATROCINIO = "LATROCINIO"
    LESAO_CORPORAL_SEGUIDA_DE_MORTE = "LESÃO CORPORAL SEGUIDA DE MORTE"
    ROUBO_A_TRANSEUNTE = "ROUBO A TRANSEUNTE"
    ROUBO_DE_VEICULO = "ROUBO DE VEICULO"
    ROUBO_EM_TRANSPORTE_COLETIVO = "ROUBO EM TRANSPORTE COLETIVO"
    ROUBO_EM_COMERCIO = "ROUBO EM COMERCIO "
    ROUBO_EM_RESIDENCIA = "ROUBO EM RESIDENCIA"
    FURTO_EM_VEICULO = "FURTO EM VEICULO"
    TENTATIVA_DE_HOMICIDIO = "TENTATIVA DE HOMICIDIO"
    TENTATIVA_DE_FEMINICIDIO = "TENTATIVA DE FEMINICIDIO"
    TENTATIVA_DE_LATROCINIO = "TENTATIVA DE LATROCINIO"
    ESTUPRO = "ESTUPRO"
    ESTUPRO_DE_VULNERAVEL = "ESTUPRO DE VULNERAVEL"
    TRAFICO_DE_DROGAS = "TRAFICO DE DROGAS"
    USO_E_PORTE_DE_DROGAS = "USO E PORTE DE DROGAS"
    POSSE_PORTE_DE_ARMA_DE_FOGO = "POSSE/PORTE DE ARMA DE FOGO"
    LOCALIZACAO_DE_VEICULO_FURTADO_OU_ROUBADO = "LOCALIZACÃO DE VEICULO FURTADO OU ROUBADO"

# --- CLASSE OCORRÊNCIAS RESPONSE  ---
class OcorrenciasResponse(BaseModel):
    id: int = Field(..., description="Identificador único da ocorrência")
    # ATUALIZAÇÃO SINTÁTICA: Usando Enum para Natureza
    Natureza: NaturezaOcorrencia = Field(..., description="Natureza da ocorrência")
    Mes: int = Field(..., ge=1, le=12, description="Mês da ocorrência (1-12)")
    Ano: int = Field(..., ge=2000, le=2100, description="Ano da ocorrência (2000-2100)")
    Quantidade: int = Field(..., description="Quantidade de ocorrências")
    # ATUALIZAÇÃO SINTÁTICA: Usando model_config (Pydantic v2)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "Natureza": "Roubo",
                "Mes": 6, "Ano": 2024,
                "Quantidade": 10
                    }})

# Schema de Resposta de Sucesso para o POST (Confirmação)
class SuccessMessage(BaseModel):
    message: str = Field(..., description="Mensagem de sucesso da operação")


#Schema de Requisição Natureza
class NaturezaRequest(BaseModel):
    codigo: int = Field(
        ...,
        gt=0,
        description="Código da Natureza da ocorrência"
        )

#Schema de Resposta Natureza
class NaturezaResponse(BaseModel):
    cod_natureza: int = Field(..., description="Código da Natureza da ocorrência")
    natureza: str = Field(..., description="Natureza da ocorrência")