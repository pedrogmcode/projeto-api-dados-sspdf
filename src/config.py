'''
Configuracoes da aplicacao
Centraliza as variáveis de configuração
'''

from pathlib import Path

'''
Configurações da API
'''
# Caminhos
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "src" / "data" / "DadosOcorrencias.xlsx"

# Informações da API
API_TITLE = "API de Consulta Estatística"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API para consultar estatísticas de ocorrências"
