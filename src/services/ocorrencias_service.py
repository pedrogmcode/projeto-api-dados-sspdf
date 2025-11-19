

import pandas as pd
from src.models.model_loader import save_new_record
from src.schemas.schemas import OcorrenciasRequest


def cadatrar_ocorrencias(request: OcorrenciasRequest):
    """
    Recebe a requisição Pydantic e orquestra a inserção do dado no CSV.
    """
    # 1. Converte o objeto Pydantic para um formato que o Pandas entenda
    new_data_dict = request.model_dump()
    
    # 2. Renomear chaves para corresponder ao CSV/modelo interno
    new_data_dict['MÊS'] = new_data_dict.pop('mes')
    new_data_dict['ANO'] = new_data_dict.pop('ano')
   # new_data_dict['NATUREZA'] = new_data_dict.pop('cod_natureza')
    new_data_dict['COD_NATUREZA'] = new_data_dict.pop('cod_natureza')
    new_data_dict['RA'] = new_data_dict.pop('id_ra')
    new_data_dict['ID_RA'] = new_data_dict.pop('id_ra')
    new_data_dict['QUANTIDADE'] = new_data_dict.pop('quantidade')

    # 3. Cria um DataFrame de um registro para a função de salvamento
    new_record_df = pd.DataFrame([new_data_dict])
    
    # 4. Chama a camada de acesso a dados (o seu model_loader)
    save_new_record(new_record_df)
    
    return {"message": "Registro inserido com sucesso."}