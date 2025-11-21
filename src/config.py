# src/config.py
# Configurações da aplicação - centralização de variáveis de configuração
# Autor: Casimiro
# Data: 2025-11-17

import logging
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- 1. CONFIGURAÇÃO DE VARIAVEIS DE AMBIENTE ---
class Settings(BaseSettings):
    # Model_config instrui o Pydantic a carregar as variaveis do arquivo .env
    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8', 
        extra='ignore' # Ignora variáveis que estejam no .env mas não nesta classe
    )

    # Variaveis que serao lidas do .env (se existirem) ou usam o valor padrao
    API_TITLE: str = "API Dados de Segurança Pública SSP/DF"
    API_VERSION: str = "1.0.0"

    # NOVAS VARIAVEIS PARA OS NOMES DOS CSVs
    CSV_NAME_CONSOLIDADO: str = "dados_consolidados_normalizado.csv"
    CSV_NAME_NATUREZA: str = "tabela_natureza_ocorrencia.csv"
    CSV_NAME_RA: str = "tabela_ra_ocorrencia.csv"

    # Variaveis de Segurança (Exemplo)
    CORS_ORIGINS: str = "http://localhost:8000" # Origens permitidas (pode ser lista)


# Instancia as configurações e carrega os dados do .env
settings = Settings()

# --- 2. DEFINIÇÃO DE CAMINHOS BASEADOS EM SETTINGS ---

# Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent 

# Caminhos usando as variaveis lidas do .env
DATA_DIR_CONSOLIDADO = BASE_DIR / "src" / "data" / settings.CSV_NAME_CONSOLIDADO
DATA_DIR_NATUREZA = BASE_DIR / "src" / "data" / settings.CSV_NAME_NATUREZA
DATA_DIR_RA = BASE_DIR / "src" / "data" / settings.CSV_NAME_RA
DATA_DIR_COMPLETO_NORMALIZADO = BASE_DIR / "src" / "data" / "dados_consolidados_normalizado.csv"

# Nomes das variaveis globais da API (usadas no main.py)
API_TITLE = settings.API_TITLE
API_VERSION = settings.API_VERSION
API_DESCRIPTION = "API para consulta de dados de segurança pública."

'''
CONFIGURAÇÃO ANTIGA DOS CAMINHOS
# CAMINHOS

# Caminho para os arquivos de dados CSV
DATA_DIR = BASE_DIR / "src" / "data" / "crimes_df_ssp_2024.csv"
DATA_DIR_COMPLETO_NORMALIZADO = BASE_DIR / "src" / "data" / "dados_consolidados_normalizado.csv"
DATA_DIR_NATUREZA = BASE_DIR / "src" / "data" / "tabela_natureza_ocorrencia.csv"
DATA_DIR_RA = BASE_DIR / "src" / "data" / "tabela_ra_ocorrencia.csv"

# Informações da API
API_TITLE = "API Dados de Segurança Pública SSP/DF"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API para consultar informações sobre ocorrências"
'''

# Configurações de logging
# Nível de log padrão
LOG_LEVEL = logging.INFO
# Formato do log
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# Diretório de logs
LOG_DIR = Path("logs")

# Criar diretório de logs se não existir
LOG_DIR.mkdir(exist_ok=True)

# Configuração do sistema de logging da aplicação
def setup_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_DIR / "app.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("ml_api")

# Logger global
logger = setup_logging()
logger.info("Logging configurado com sucesso")
