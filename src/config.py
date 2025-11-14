'''
Configuracoes da aplicacao
Centraliza as variáveis de configuração
'''

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    '''
    Configurações da API
    '''

    # Informações da API
    app_name: str = "API de Gerenciamento de Tarefas"
    app_version: str = "1.0.0"

    # Configurações de servidor
    host: str = "0.0.0.0"
    port: int = 8000

    #Modo de desenvolvimento
    debug: bool = True

    class Config:
        env_file = ".env" # Pode usar arquivo .env para variáveis

# Instância global de configurações
settings = Settings()