"""
Testes Automatizados - API FastAPI para dados de segurança públic
Estrutura AAA: Arrange, Act, Assert
"""

from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status
from ..main import app

client = TestClient(app)

def test_health_check():
    """
    Teste básico: verificar se a API está funcionando
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Funcionando!"

def test_cadastrar_ocorrencias():
    """
    Teste: Cadastrar ocorrências (Payload Válido - 201 Created)
    """
    # ARRANGE
    payload = {
        "ano": 2024,
        "cod_natureza": 1,
        "id_ra": 1,
        "mes": 6,
        "quantidade": 10
    }
    
    # ACT
    response = client.post("/ocorrencias", json=payload)
    
    # ASSERT
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Ocorrências registradas com sucesso!"

# ----------------------------------------------------------------------
# NOVOS TESTES PARA VALIDAÇÃO (STATUS 422)
# ----------------------------------------------------------------------

# Payload base com valores válidos para usar nos testes de exceção
VALID_PAYLOAD = {
    "ano": 2024,
    "cod_natureza": 1,
    "id_ra": 1,
    "mes": 6,
    "quantidade": 10
}

def test_validacao_id_ra_min():
    """
    Testa id_ra < 1 (ge=1)
    """
    payload = VALID_PAYLOAD.copy()
    payload["id_ra"] = 0 # Valor inválido
    response = client.post("/ocorrencias", json=payload)
    assert response.status_code == 422
    # Opcional: Assert para verificar a mensagem de erro específica do Pydantic
    assert response.json()["detail"][0]["loc"][1] == "id_ra"
    assert "greater than or equal to 1" in response.json()["detail"][0]["msg"]

def test_validacao_id_ra_max():
    """
    Testa id_ra > 33 (le=33)
    """
    payload = VALID_PAYLOAD.copy()
    payload["id_ra"] = 34 # Valor inválido
    response = client.post("/ocorrencias", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "id_ra"
    assert "less than or equal to 33" in response.json()["detail"][0]["msg"]

def test_validacao_cod_natureza_min():
    """
    Testa cod_natureza < 1 (ge=1)
    """
    payload = VALID_PAYLOAD.copy()
    payload["cod_natureza"] = 0 # Valor inválido
    response = client.post("/ocorrencias", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "cod_natureza"
    assert "greater than or equal to 1" in response.json()["detail"][0]["msg"]

def test_validacao_cod_natureza_max():
    """
    Testa cod_natureza > 32 (le=32)
    """
    payload = VALID_PAYLOAD.copy()
    payload["cod_natureza"] = 33 # Valor inválido
    response = client.post("/ocorrencias", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "cod_natureza"
    assert "less than or equal to 32" in response.json()["detail"][0]["msg"]

def test_validacao_quantidade_min():
    """
    Testa quantidade < 0 (ge=0)
    """
    payload = VALID_PAYLOAD.copy()
    payload["quantidade"] = -1 # Valor inválido
    response = client.post("/ocorrencias", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "quantidade"
    assert "greater than or equal to 0" in response.json()["detail"][0]["msg"]

def test_validacao_mes_min():
    """
    Testa mes < 1 (ge=1)
    """
    payload = VALID_PAYLOAD.copy()
    payload["mes"] = 0 # Valor inválido
    response = client.post("/ocorrencias", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "mes"
    assert "greater than or equal to 1" in response.json()["detail"][0]["msg"]

def test_validacao_mes_max():
    """
    Testa mes > 12 (le=12)
    """
    payload = VALID_PAYLOAD.copy()
    payload["mes"] = 13 # Valor inválido
    response = client.post("/ocorrencias", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "mes"
    assert "less than or equal to 12" in response.json()["detail"][0]["msg"]

def test_validacao_ano_min():
    """
    Testa ano < 2000 (ge=2000)
    """
    payload = VALID_PAYLOAD.copy()
    payload["ano"] = 1999 # Valor inválido
    response = client.post("/ocorrencias", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "ano"
    assert "greater than or equal to 2000" in response.json()["detail"][0]["msg"]

def test_validacao_ano_max():
    """
    Testa ano > 2100 (le=2100)
    """
    payload = VALID_PAYLOAD.copy()
    payload["ano"] = 2101 # Valor inválido
    response = client.post("/ocorrencias", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "ano"
    assert "less than or equal to 2100" in response.json()["detail"][0]["msg"]

def test_root_endpoint():
    """
    Testa o endpoint raiz (GET /)
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "API Dados de Segurança Pública funcionando!" in data["message"]
    assert "version" in data

# NOTE: Estamos mockando 'buscar_natureza' que DEVE ser importado do main.py
@patch('src.api.main.buscar_natureza')
def test_get_natureza_sucesso(mock_buscar_natureza):
    """
    CORRIGIDO: Testa a busca de uma natureza com código válido (ex: 1).
    O erro 404 foi corrigido pelo mock, que agora retorna 200 OK.
    """
    # Configura o mock para retornar um valor válido
    mock_buscar_natureza.return_value = NATUREZA_MOCK

    codigo_valido = 1
    response = client.get(f"/natureza/{codigo_valido}")
    
    # AGORA ESPERAMOS 200 OK
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["cod_natureza"] == codigo_valido
    assert data["natureza"] == NATUREZA_MOCK

def test_get_natureza_nao_encontrado():
    """
    Testa a busca com um código que não existe (deve retornar 404)
    """
    # ARRANGE: Código muito alto, que provavelmente não existe
    codigo_nao_existente = 999 
    
    # ACT
    response = client.get(f"/natureza/{codigo_nao_existente}")
    
    # ASSERT
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "não encontrado" in response.json()["detail"]

def test_get_natureza_codigo_invalido_min():
    """
    Testa a validação do Path Parameter: codigo <= 0 (deve retornar 422)
    """
    # ARRANGE
    codigo_invalido = 0 
    
    # ACT
    response = client.get(f"/natureza/{codigo_invalido}")
    
    # ASSERT
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # Verifica se a validação falhou no Path Parameter 'codigo'
    assert response.json()["detail"][0]["loc"][0] == "path"
    assert response.json()["detail"][0]["loc"][1] == "codigo"

# ----------------------------------------------------------------------
# NOVOS TESTES PARA ENDPOINT /ocorrencias_media
# ----------------------------------------------------------------------

# NOTE: Estes testes assumem que 'get_media_historica' é capaz de retornar
#       dados mockados ou que o banco de dados/CSV contém dados para o filtro.

VALID_MEDIA_QUERY = {
    "id_ra": 1, 
    "ano": 2023, 
    "mes": 1, 
    "cod_natureza": 7 
}

def test_ocorrencias_media_sucesso():
    """
    Testa o cálculo da média com parâmetros válidos (GET /ocorrencias_media)
    """
    # ARRANGE: Use um filtro válido
    params = VALID_MEDIA_QUERY
    
    # ACT
    # Passamos os parâmetros diretamente na URL
    response = client.get("/ocorrencias_media", params=params)
    
    # ASSERT
    # Assume-se que a camada de serviço retorna 200 OK com dados válidos
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data["Media_Historica_Mes"], float)
    assert data["ID_RA"] == 1
    assert data["COD_NATUREZA"] == 7
    # Verifica se todos os campos estão presentes (conforme OcorrenciasMediaResponse)
    assert all(key in data for key in ["MES", "ANO", "Natureza", "RegiaoAdministrativa", "Quantidade_Atual"])


def test_ocorrencias_media_nao_encontrado():
    """
    Testa o caso em que o serviço retorna ValueError (deve ser 404)
    Isso simula o bloco 'except ValueError as e:' no seu código
    """
   
    params = {
        "id_ra": 1, 
        "ano": 2023, 
        "mes": 1, 
        "cod_natureza": 999 
    }
    
    # ACT
    response = client.get("/ocorrencias_media", params=params)
    
    if response.status_code != status.HTTP_200_OK:
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
# --- Testes de Validação do GET /ocorrencias_media (422) ---

def test_ocorrencias_media_validacao_mes_min():
    """
    Testa a validação do Query Parameter: mes < 1 (ge=1)
    """
    params = VALID_MEDIA_QUERY.copy()
    params["mes"] = 0 # Valor inválido
    
    response = client.get("/ocorrencias_media", params=params)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["loc"][1] == "mes"

def test_ocorrencias_media_validacao_id_ra_max():
    """
    Testa a validação do Query Parameter: id_ra > 33 (le=33)
    """
    params = VALID_MEDIA_QUERY.copy()
    params["id_ra"] = 34 # Valor inválido
    
    response = client.get("/ocorrencias_media", params=params)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["loc"][1] == "id_ra"

def test_ocorrencias_media_validacao_ano_min():
    """
    Testa a validação do Query Parameter: ano < 2000 (ge=2000)
    """
    params = VALID_MEDIA_QUERY.copy()
    params["ano"] = 1999 # Valor inválido
    
    response = client.get("/ocorrencias_media", params=params)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["loc"][1] == "ano"

def test_ocorrencias_media_validacao_ano_max():
    """ Testa a validação do Query Parameter: ano > 2100 (le=2100). """
    params = VALID_MEDIA_QUERY.copy()
    params["ano"] = 2101
    response = client.get("/ocorrencias_media", params=params)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["loc"][1] == "ano"

# --- mes ---
def test_ocorrencias_media_validacao_mes_min():
    """ Testa a validação do Query Parameter: mes < 1 (ge=1). """
    params = VALID_MEDIA_QUERY.copy()
    params["mes"] = 0
    response = client.get("/ocorrencias_media", params=params)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["loc"][1] == "mes"

def test_ocorrencias_media_validacao_mes_max():
    """ Testa a validação do Query Parameter: mes > 12 (le=12). """
    params = VALID_MEDIA_QUERY.copy()
    params["mes"] = 13
    response = client.get("/ocorrencias_media", params=params)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["loc"][1] == "mes"

# --- cod_natureza ---
def test_ocorrencias_media_validacao_cod_natureza_min():
    """ Testa a validação do Query Parameter: cod_natureza < 1 (ge=1). """
    params = VALID_MEDIA_QUERY.copy()
    params["cod_natureza"] = 0
    response = client.get("/ocorrencias_media", params=params)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["loc"][1] == "cod_natureza"
    
# Dados de MOCK para Natureza
NATUREZA_MOCK = "ESTUPRO"

# Dados de MOCK para Média Histórica (conforme OcorrenciasMediaResponse)
MEDIA_MOCK_RESPONSE = {
    "MES": 1,
    "ANO": 2023,
    "Natureza": "HOMICÍDIO",
    "RegiaoAdministrativa": "ARNIQUEIRA",
    "Quantidade_Atual": 10,
    "Media_Historica_Mes": 8.5,
    "ID_RA": 1,
    "COD_NATUREZA": 7
}