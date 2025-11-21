# Arquivo: main.py
# Ponto de entrada da API FastAPI para dados de segurança pública
# Autor: Casimiro
# Data: 2025-11-15

import random
from typing import List

from fastapi import FastAPI, HTTPException, status, Path, Query

from src.config import settings, API_DESCRIPTION, API_TITLE, API_VERSION, logger 
from fastapi.middleware.cors import CORSMiddleware # <--- NOVO IMPORT
from src.schemas.schemas import OcorrenciasRequest, OcorrenciasResponse, SuccessMessage, NaturezaResponse, Ocorrencias_Nomes_Response, OcorrenciasMediaResponse
#from src.models.model_loader import filter_ocorrencias
from src.services import ocorrencias_service
from src.services.ocorrencias_service import get_ocorrencias_nomes_filtradas, get_media_historica


app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# ----------------------------
# --- CONFIGURAÇÃO DO CORS ---
# ----------------------------

# Converte a string de origens do .env para uma lista de Python
origins = settings.CORS_ORIGINS.split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Lista de domínios permitidos (lidos do .env)
    allow_credentials=True,            # Permite cookies e cabeçalhos de autorização
    allow_methods=["*"],               # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],               # Permite todos os cabeçalhos
)


# ---------------------
# --- Endpoint raiz ---
# ---------------------

@app.get("/")
def root():
    logger.info("Endpoint raiz acessado")
    return {
        "message": "API Dados de Segurança Pública funcionando!",
        "version": API_VERSION
    }
# -----------------------------
# --- Health Check Endpoint ---
# -----------------------------

@app.get("/health")
def health_check():
    logger.info("Health check realizado!")
    return {
        "status": "Funcionando!",
        "service": API_TITLE,
        "version": API_VERSION
    }
# --------------------------------------------
# --- ENDPOINT DE CONSULTA COM NOMES (GET) ---
# --------------------------------------------

@app.get("/ocorrencias_nomes", response_model=List[Ocorrencias_Nomes_Response])
def ocorrencias_nomes(
    # Query: Usado para definir parâmetros obrigatórios na URL
    id_ra: int = Query(..., description="ID da Região Administrativa para filtro.", ge=1, le=33),
    ano: int = Query(..., ge=2000, le=2100, description="Ano da ocorrência."),
    mes: int = Query(..., ge=1, le=12, description="Mês da ocorrência."),
):
    logger.info(f"Consulta Nomes solicitada: ID_RA={id_ra}, Ano={ano}, Mês={mes}")

    # Delega a filtragem para a camada de Serviço
    dados_filtrados = get_ocorrencias_nomes_filtradas(id_ra=id_ra, ano=ano, mes=mes)

    if not dados_filtrados:
         # Retorna 404 Not Found se não houver resultados
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma ocorrência encontrada para os filtros fornecidos.")

    return dados_filtrados

'''# Endpoint de Ocorrências (Requisição GET)
# Recebe Mês e Ano como query parameters, e retorna uma lista de ocorrências filtradas.
@app.get("/Ocorrencias", response_model=List[OcorrenciasResponse])
# FastAPI usa os parâmetros da URL para validar o Esquema Pydantic!
# A função recebe Mes e Ano diretamente, mas a validação do Pydantic (ge, le) funciona.
def Ocorrencias(Mes: int,Ano: int):
    logger.info(f"Ocorrências solicitadas com Mês: {Mes}, Ano: {Ano}")

    # Adaptar a Requisição para a Função de Filtragem
    # A função filter_ocorrencias espera um objeto OcorrenciasRequest,
    # Necessário criar a partir dos parâmetros de consulta (Mes, Ano).
    request_data = OcorrenciasRequest(mes=Mes, ano=Ano)

    # Chamar a função de filtragem
    ocorrencias_filtradas = filter_ocorrencias(request_data)

    # Retorna a lista de objetos Pydantic
    return ocorrencias_filtradas
'''

# --------------------------------------------
# --- ENDPOINT DE CADASTRO DE OCORRENCIAS (POST) ---
# --------------------------------------------

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


# ----------------------------------------------------
# --- ENDPOINT DE CÁLCULO DE MÉDIA HISTÓRICA (GET) ---
# ----------------------------------------------------

@app.get("/ocorrencias_media", response_model=OcorrenciasMediaResponse)
def ocorrencias_media(
    # Parâmetros obrigatórios e validados na URL
    id_ra: int = Query(..., description="ID da Região Administrativa para filtro.", ge=1, le=33),
    ano: int = Query(..., ge=2000, le=2100, description="Ano da ocorrência."),
    mes: int = Query(..., ge=1, le=12, description="Mês da ocorrência."),
    cod_natureza: int = Query(..., description="Código da Natureza para cálculo da média.", ge=1)
):
    logger.info(f"Consulta Média Histórica solicitada: RA={id_ra}, Ano={ano}, Mês={mes}, Natureza={cod_natureza}")

    try:
        # Delega o cálculo para a camada de Serviço
        dados_media = get_media_historica(
            id_ra=id_ra,
            ano=ano,
            mes=mes,
            cod_natureza=cod_natureza
        )
        return dados_media

    except ValueError as e:
        # Trata o erro de 404 Not Found se o filtro não encontrar dados
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.error(f"Erro inesperado no cálculo da média: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao calcular a média histórica.")


