# Arquivo: main.py
# Ponto de entrada da API FastAPI para dados de segurança pública
# Autor: Casimiro
# Data: 2025-11-15

from typing import List

from fastapi import FastAPI

from src.config import API_DESCRIPTION, API_TITLE, API_VERSION, logger
from src.schemas.schemas import OcorrenciasRequest, OcorrenciasResponse
from src.models.model_loader import filter_ocorrencias

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
#Endpoint para cadastro de quantidade de ocorrências
@app.post("/Ocorrencias", response_model=List[OcorrenciasRequest])
def Ocorrencias(input_data: OcorrenciasRequest):
    """
    Endpoint para cadastro de quantidade de ocorrências.
    """
    logger.info(f"Requisição POST recebida com Mês: {input_data.Mes}, Ano: {input_data.Ano}, Quantidade: {input_data.quantidade}, Natureza: {input_data.cod_natureza}, RA: {input_data.id_ra}")
    