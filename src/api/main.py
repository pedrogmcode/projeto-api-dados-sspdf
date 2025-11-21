# Arquivo: main.py
# Ponto de entrada da API FastAPI para dados de segurança pública
# Autor: Casimiro
# Data: 2025-11-15

import random
from typing import List

from fastapi import FastAPI, HTTPException, status, Path

from src.config import API_DESCRIPTION, API_TITLE, API_VERSION, logger
from src.schemas.schemas import OcorrenciasRequest, OcorrenciasResponse, SuccessMessage, NaturezaResponse
from src.models.model_loader import filter_ocorrencias, buscar_natureza
from src.services import ocorrencias_service

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Endpoint raiz
@app.get("/")
def root():
    logger.info("Endpoint raiz acessado")
    return {
        "message": "API Dados de Segurança Pública funcionando!",
        "version": API_VERSION
    }

# Health Check Endpoint
@app.get("/health")
def health_check():
    logger.info("Health check realizado!")
    return {
        "status": "Funcionando!",
        "service": API_TITLE,
        "version": API_VERSION
    }

# Endpoint de Ocorrências (Requisição GET)
# Recebe Mês e Ano como query parameters, e retorna uma lista de ocorrências filtradas.
@app.get("/Ocorrencias", response_model=List[OcorrenciasResponse])
# FastAPI usa os parâmetros da URL para validar o Esquema Pydantic!
# A função recebe Mes e Ano diretamente, mas a validação do Pydantic (ge, le) funciona.
def Ocorrencias(Mes: int,Ano: int):
    logger.info(f"Ocorrências solicitadas com Mês: {Mes}, Ano: {Ano}")

    # Adaptar a Requisição para a Função de Filtragem
    # A função filter_ocorrencias espera um objeto OcorrenciasRequest,
    # Necessário criar a partir dos parâmetros de consulta (Mes, Ano).
    request_data = OcorrenciasRequest(Mes=Mes, Ano=Ano)

    # Chamar a função de filtragem
    ocorrencias_filtradas = filter_ocorrencias(request_data)

    # Retorna a lista de objetos Pydantic
    return ocorrencias_filtradas

'''
# Inutilizado por Casimiro em 17-11-2025

# Endpoint de Ocorrências (POST)
# Recebe Mês e Ano, e retorna um exemplo de ocorrência validada.
# Em um projeto real, esta função consultaria o DataFrame ou um modelo.

# Endpoint de Ocorrências (Requisição POST)
# Recebe Mês e Ano, e retorna uma lista de ocorrências filtradas.
@app.post("/Ocorrencias", response_model=List[OcorrenciasResponse])
def Ocorrencias(input_data: OcorrenciasRequest):
    logger.info(f"Ocorrências solicitadas com Mês: {input_data.Mes}, Ano: {input_data.Ano}")
    # Chama a função de filtragem
    ocorrencias_filtradas = filter_ocorrencias(input_data)
    # Retorna a lista de objetos Pydantic
    # Alteramos o response_model do decorador para List[OcorrenciasResponse]
    return ocorrencias_filtradas
'''
# Endpoint para cadastro de quantidade de ocorrências (POST)
@app.post("/ocorrencias", 
          response_model=SuccessMessage, 
          status_code=status.HTTP_201_CREATED,
          summary="Cadastra novas ocorrências.")
def adicionar_ocorrencias(input_data: OcorrenciasRequest):
    """
    Recebe os dados de ocorrências, valida o formato e registra no CSV.
    Retorna objeto salvo.
    """
    try:
        # Delega a lógica de persistência para a camada de Serviço
        ocorrencias_service.cadatrar_ocorrencias(input_data)
        
        # Retorna o modelo de resposta de sucesso
        return SuccessMessage(message="Ocorrências registradas com sucesso!")
    
    except Exception as e:
        # Se ocorrer um erro durante a escrita do CSV, retorna 500
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao registrar a ocorrências: {e}"
        )
    
#Endpoint para busca das naturezas disponíveis
@app.get("/natureza/{codigo}", response_model=NaturezaResponse)
def get_natureza(codigo: int = Path(..., gt=0, description="Código da natureza da ocorrência")):

    """
    Retorna a natureza correspondente ao código informado.
    Converte para string porque a função buscar_natureza espera receber uma string.
    """
    natureza = buscar_natureza(str(codigo))

    if natureza is None:
        raise HTTPException(status_code=404, detail="Código de natureza não encontrado")

    return NaturezaResponse(cod_natureza=codigo, natureza=natureza)