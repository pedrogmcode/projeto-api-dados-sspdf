'''
Configuracoes da aplicacao
Centraliza as variáveis de configuração
'''

from pathlib import Path
import logging
from pathlib import Path

#CONFIGURAÇÕES DA API

# CAMINHOS
# Diretório base do projeto
BASE_DIR = Path(__file__).parent.parent  # Dois níveis acima do arquivo atual
# Caminho para o arquivo de dados CSV
DATA_DIR = BASE_DIR / "src" / "data" / "crimes_df_ssp_2024.csv"


# Informações da API
API_TITLE = "API Dados de Segurança Pública SSP/DF"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API para consultar informações sobre ocorrências"

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