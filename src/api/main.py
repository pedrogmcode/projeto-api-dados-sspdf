# Arquivo: main.py

from typing import List

from fastapi import FastAPI

from src.config import API_DESCRIPTION, API_TITLE, API_VERSION, logger
from src.data.schemas import OcorrenciasRequest, OcorrenciasResponse
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

# Endpoint de Ocorrências (Requisição POST)
# Recebe Mês e Ano, e retorna um exemplo de ocorrência validada.
# Em um projeto real, esta função consultaria o DataFrame ou um modelo.

# Endpoint de Ocorrências (Requisição POST)
@app.post("/Ocorrencias", response_model=List[OcorrenciasResponse])
def Ocorrencias(input_data: OcorrenciasRequest):
    """
    Consulta o DataFrame carregado e retorna as ocorrências filtradas por Mês e Ano.
    """
    logger.info(f"Ocorrências solicitadas com Mês: {input_data.Mes}, Ano: {input_data.Ano}")
    
    # 1. Chama a função de filtragem
    ocorrencias_filtradas = filter_ocorrencias(input_data)
    
    # 2. Retorna a lista de objetos Pydantic
    # Nota: Alteramos o response_model do decorador para List[OcorrenciasResponse]
    return ocorrencias_filtradas
