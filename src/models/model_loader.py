# Arquivo: src/models/model_loader.py

#from functools import lru_cache
from typing import List

import pandas as pd

from src.config import DATA_DIR, logger
from src.data.schemas import OcorrenciasRequest, OcorrenciasResponse


#@lru_cache(maxsize=1)
def load_data_ocorrencias() -> pd.DataFrame:
    """
    Carrega o dataset de ocorrências do DF em memória.
    Retorna um DataFrame com nomes de colunas padronizados (snake_case).
    """
    logger.info(f"Tentando carregar dados do caminho: {DATA_DIR}")
    try:
        # 1. Carregamento: Usando sep=';' conforme o seu CSV
        df = pd.read_csv(DATA_DIR, sep=';', encoding='utf-8') 
        
        # 2. Padronização: minúsculo e snake_case para acesso seguro
        df.columns = df.columns.str.lower().str.replace(' ', '_')
        
        # 3. Conversão de Tipos: Necessário para o filtro
        df['mes'] = df['mes'].astype(int)
        df['ano'] = df['ano'].astype(int)
        
        logger.info(f"Dados de ocorrências carregados com sucesso: {df.shape[0]} linhas.")
        return df
        
    except FileNotFoundError:
        # Trata o erro de não encontrar o CSV (causa mais comum do erro 500)
        logger.error(f"ERRO: Arquivo CSV não encontrado em {DATA_DIR}. Verifique o caminho.")
        return pd.DataFrame()
    except KeyError as e:
        # Trata erro de colunas, caso o CSV não tenha 'mes' ou 'ano'
        logger.error(f"ERRO: Coluna {e} não encontrada. Verifique o CSV.")
        return pd.DataFrame()
    except Exception as e:
        # Trata erros genéricos de carregamento (ex: problemas de encoding)
        logger.error(f"ERRO inesperado ao carregar ou processar CSV: {e}")
        return pd.DataFrame()


def filter_ocorrencias(request: OcorrenciasRequest) -> List[OcorrenciasResponse]:
    """
    Filtra o DataFrame carregado com base no Mês e Ano da requisição
    e converte os resultados filtrados para o formato Pydantic.
    """
    df_ocorrencias = load_data_ocorrencias()
    
    # 1. Verificação de Segurança (Se o carregamento falhou, retorna lista vazia)
    if df_ocorrencias.empty:
        return []
    
    # 2. Aplicar Filtro: Usa as colunas padronizadas ('mes' e 'ano')
    df_filtrado = df_ocorrencias[
        (df_ocorrencias['mes'] == request.Mes) & 
        (df_ocorrencias['ano'] == request.Ano)
    ].copy() # O .copy() é uma boa prática para evitar warnings do Pandas
    
    logger.info(f"Encontrados {len(df_filtrado)} registros para {request.Mes}/{request.Ano}.")
    
    # 3. Renomear e Selecionar Colunas para o Pydantic (CapCase)
    # Mapeia colunas do Pandas (snake_case) para o Pydantic (CapCase)
    df_filtrado = df_filtrado.rename(columns={
        'natureza': 'Natureza', 
        'mes': 'Mes', 
        'ano': 'Ano'
    })
    
    # Seleciona apenas as colunas que o Pydantic espera (id, Natureza, Mes, Ano)
    dados_filtrados_dict = df_filtrado[['id', 'Natureza', 'Mes', 'Ano']].to_dict('records')
    
    # 4. Cria os objetos Pydantic
    # Garante que cada item da lista está validado pelo OcorrenciasResponse
    response_list = [OcorrenciasResponse(**item) for item in dados_filtrados_dict]
    
    return response_list