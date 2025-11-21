
# Arquivo: src/services/ocorrencias_service.py

from typing import List, Dict, Any
import pandas as pd
from src.models.model_loader import save_new_record, load_denormalized_data 
from src.schemas.schemas import OcorrenciasRequest, Ocorrencias_Nomes_Response, OcorrenciasMediaResponse
from src.config import logger

# ------------------------------------------
# --- FUNÇÃO DE INSERÇÃO DE DADOS NO CSV ---
# ------------------------------------------

def cadatrar_ocorrencias(request: OcorrenciasRequest):
    """
    Recebe a requisição Pydantic e orquestra a inserção do dado no CSV.
    """
    # 1. Converte o objeto Pydantic para um formato que o Pandas entenda
    new_data_dict = request.model_dump()

    # 2. Renomear chaves para corresponder ao CSV/modelo interno
    new_data_dict['MES'] = new_data_dict.pop('mes')
    new_data_dict['ANO'] = new_data_dict.pop('ano')
    new_data_dict['COD_NATUREZA'] = new_data_dict.pop('cod_natureza')
    new_data_dict['ID_RA'] = new_data_dict.pop('id_ra')
    new_data_dict['QUANTIDADE'] = new_data_dict.pop('quantidade')

    # 3. Cria um DataFrame de um registro para a função de salvamento
    new_record_df = pd.DataFrame([new_data_dict])

    # 4. Chama a camada de acesso a dados (o seu model_loader)
    save_new_record(new_record_df)

    return {"message": "Registro inserido com sucesso."}

# -------------------------------------------
# --- FUNÇÃO DE CONSULTA OCORRÊNCIAS(GET) ---
# -------------------------------------------

def get_ocorrencias_nomes_filtradas(id_ra: int, ano: int, mes: int) -> List[Ocorrencias_Nomes_Response]:
    """
    Filtra os dados DENORMALIZADOS (com nomes) pelo ID_RA, ANO e MES.
    Retorna uma lista de Ocorrencias_Nomes_Response.
    """
    # 1. Carrega os dados desnormalizados
    df_completo = load_denormalized_data()

    if df_completo.empty:
        logger.warning("Serviço de consulta Nomes falhou: DataFrame denormalizado está vazio.")
        return []

    # 2. Aplicar Filtros (usando as colunas padronizadas para minúsculo)
    df_filtrado = df_completo[
        (df_completo['id_ra'] == id_ra) &
        (df_completo['ano'] == ano) &
        (df_completo['mes'] == mes)
    ].copy()

    logger.info(f"Consulta Nomes finalizada. Registros encontrados: {len(df_filtrado)} para RA={id_ra}.")

    # 3. Formatação para Pydantic
    # Renomear colunas do DataFrame para corresponder exatamente ao Schema Pydantic:
    df_formatado = df_filtrado.rename(columns={
        'id_ra': 'ID_RA',
        'mes': 'MES',
        'ano': 'ANO',
        'cod_natureza': 'COD_NATUREZA',
        'quantidade': 'QUANTIDADE',
        'natureza': 'Natureza',
        'regiao_administrativa': 'RegiaoAdministrativa'
    })

    # 4. Converter para o modelo Pydantic
    cols_selecionadas = [
        'MES', 'ANO', 'QUANTIDADE',
        'Natureza', 'RegiaoAdministrativa',
        'ID_RA', 'COD_NATUREZA'
    ]
    dados_dict = df_formatado[cols_selecionadas].to_dict('records')

    response_list = [Ocorrencias_Nomes_Response(**item) for item in dados_dict]

    return response_list

# ------------------------------------
# --- FUNÇÃO GET OCORRÊNCIAS MÉDIA ---
# ------------------------------------

def get_media_historica(id_ra: int, ano: int, mes: int, cod_natureza: int) -> OcorrenciasMediaResponse:
    """
    Calcula a quantidade atual de ocorrências e a média histórica
    para um Mês/Natureza/RA, considerando todos os anos disponíveis.
    """
    # 1. Carrega os dados desnormalizados (cache garante rapidez)
    df_completo = load_denormalized_data()

    if df_completo.empty:
        logger.warning("Serviço de Média Histórica falhou: DataFrame denormalizado está vazio.")
        raise ValueError("Dados não carregados.")

    # 2. DEFINIR FILTROS CHAVE
    # Filtro 1: Ocorrência Específica (Mês, Ano, RA, Natureza)
    filtro_especifico = (
        (df_completo['id_ra'] == id_ra) &
        (df_completo['ano'] == ano) &
        (df_completo['mes'] == mes) &
        (df_completo['cod_natureza'] == cod_natureza)
    )

    # Filtro 2: Média Histórica (Mês, RA, Natureza, TODOS os Anos)
    filtro_historico = (
        (df_completo['id_ra'] == id_ra) &
        (df_completo['mes'] == mes) &
        (df_completo['cod_natureza'] == cod_natureza)
    )

    # 3. EXTRATO DE DADOS
    df_especifico = df_completo[filtro_especifico]
    df_historico = df_completo[filtro_historico]

    if df_especifico.empty:
        logger.info("Nenhuma ocorrência encontrada para o filtro específico.")
        raise ValueError("Nenhuma ocorrência encontrada para o mês/ano/natureza/RA especificados.")

    # 4. CÁLCULO DA MÉDIA
    # A média é calculada sobre a coluna 'quantidade' do DataFrame histórico
    media_historica = df_historico['quantidade'].mean()

    # 5. EXTRAÇÃO DE DADOS (Apenas o primeiro registro específico)
    registro_atual = df_especifico.iloc[0]

    # 6. FORMATAÇÃO DO RESPONSE
    # Note que usamos o registro atual para obter os nomes descritivos
    response_data = OcorrenciasMediaResponse(
        MES=int(registro_atual['mes']),
        ANO=int(registro_atual['ano']),
        Natureza=str(registro_atual['natureza']),
        RegiaoAdministrativa=str(registro_atual['regiao_administrativa']),
        Quantidade_Atual=int(registro_atual['quantidade']),
        # Arredonda tirando as casas decimais
        Media_Historica_Mes=round(media_historica, 0),
        ID_RA=int(registro_atual['id_ra']),
        COD_NATUREZA=int(registro_atual['cod_natureza'])
    )

    return response_data
