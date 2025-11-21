# Arquivo: src/models/model_loader.py

from functools import lru_cache
from typing import List

import pandas as pd

from src.config import DATA_DIR, DATA_DIR_COMPLETO_NORMALIZADO, logger, BASE_DIR
from src.schemas.schemas import OcorrenciasRequest, OcorrenciasResponse


# Carrega o dataset de ocorrências do DF em memória.
# Retorna um DataFrame com nomes de colunas padronizados (snake_case).
@lru_cache(maxsize=1)
def load_data_ocorrencias() -> pd.DataFrame:
    logger.info(f"Tentando carregar dados do caminho: {DATA_DIR}")
    try:
        # Carregamento usando sep=';' conforme CSV
        df = pd.read_csv(DATA_DIR, sep=';', encoding='utf-8')

        # Padronização: minúsculo e snake_case para acesso seguro
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        # Conversão de Tipos: Necessário para o filtro
        df['mes'] = df['mes'].astype(int)
        df['ano'] = df['ano'].astype(int)
        # Loga número de linhas carregadas
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

# Filtrar DataFrame carregado com base no Mês e Ano da requisição
# Converter os resultados filtrados para o formato Pydantic.

# Função de filtragem
# Recebe o objeto de requisição Pydantic
# Retorna uma lista de objetos Pydantic
def filter_ocorrencias(request: OcorrenciasRequest) -> List[OcorrenciasResponse]:

    # Carrega o DataFrame (usando cache para eficiência)
    df_ocorrencias = load_data_ocorrencias()

    # Verifica por Segurança se o carregamento falhou, retorna lista vazia
    if df_ocorrencias.empty:
        return []

    # Aplicar Filtro: Usa as colunas padronizadas ('mes' e 'ano')
    df_filtrado = df_ocorrencias[
        (df_ocorrencias['mes'] == request.Mes) & (df_ocorrencias['ano'] == request.Ano)
    ].copy() # .copy() é uma boa prática para evitar warnings do Pandas

    # Loga número de registros encontrados
    logger.info(f"Encontrados {len(df_filtrado)} registros para {request.Mes}/{request.Ano}.")

    # Renomear e Selecionar Colunas para o Pydantic
    # Mapeia colunas do Pandas para o Pydantic
    df_filtrado = df_filtrado[['id', 'natureza', 'mes', 'ano', 'quantidade']].rename(
    columns={
        'natureza': 'Natureza',
        'mes': 'Mes',
        'ano': 'Ano',
        'quantidade': 'Quantidade'
            })

    # Seleciona apenas as colunas que o Pydantic espera (id, Natureza, Mes, Ano)
    dados_filtrados_dict = df_filtrado.to_dict('records')

    # Criar os objetos Pydantic
    # Garante que cada item da lista está validado pelo OcorrenciasResponse
    response_list = [OcorrenciasResponse(**item) for item in dados_filtrados_dict]

    return response_list

# Função para inserir novos dados no CSV
def save_new_record(new_df: pd.DataFrame):
    """
    Insere o DataFrame no arquivo CSV, usando o modo 'append'.
    """
    try:
        # Escreve o novo DataFrame no arquivo
        new_df.to_csv(
            DATA_DIR_COMPLETO_NORMALIZADO, 
            mode='a', # Abre o arquivo em modo 'append' (adicionar ao final)
            sep=';', 
            encoding='utf-8', 
            header=False, # Não escreve o cabeçalho novamente
            index=False   # Não escreve o índice do DataFrame
        )
        # Limpa o cache do leitor para que a próxima leitura recarregue o dado novo
        load_data_ocorrencias.cache_clear()
        logger.info(f"Novo registro salvo com sucesso no CSV: {new_df.shape[0]} linhas.")

    except Exception as e:
        logger.error(f"ERRO ao salvar novo registro no CSV: {e}")
        # Lançar exceção ou tratar erro
        raise

#Carregar a lista de Naturezas disponíveis
@lru_cache(maxsize=1)
def load_naturezas() -> pd.DataFrame:
    logger.info(f"Tentando carregar dados de naturezas do caminho: {BASE_DIR / 'src' / 'data' / 'tabela_natureza_ocorrencia.csv'}")
    try:
        df = pd.read_csv(
            BASE_DIR / "src" / "data" / "tabela_natureza_ocorrencia.csv",
            sep=';', 
            encoding='latin1')
        
        #Padronização: minúsculo e snake_case para acesso seguro
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        #Converte COD_NATUREZA para int para evitar problemas de comparação
        df['cod_natureza'] = df['cod_natureza'].astype(int)

        logger.info(f"Dados de naturezas carregados com sucesso: {df.shape[0]} linhas.")
        return df

    except FileNotFoundError:
        logger.error(f"ERRO: Arquivo CSV de naturezas não encontrado em {BASE_DIR / 'src' / 'data' / 'tabela_natureza_ocorrencia.csv'}. Verifique o caminho.")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"ERRO inesperado ao carregar ou processar CSV de naturezas: {e}")
        return pd.DataFrame()


# Função para carregar a lista de Naturezas disponíveis
def buscar_natureza(cod_natureza: str) -> str | None:
    """Busca a natureza pelo código. Retorna None se não encontrar."""
    df_naturezas = load_naturezas()

    #Verifica se o DataFrame está vazio
    if df_naturezas.empty:
        return None
    
    try:
        #Converte o código para int para comparação
        cod_natureza_int = int(cod_natureza)
        resultado = df_naturezas[df_naturezas['cod_natureza'] == cod_natureza_int]

        if resultado.empty:
            return None
        
        return resultado.iloc[0]['natureza']
    
    except ValueError:
        #Se não for possível converter para int, retorna None
        logger.warning(f"Código de natureza inválido (não é um número): {cod_natureza}")
        return None