"""
Testes Automatizados - API FastAPI para dados de segurança públic
Estrutura AAA: Arrange, Act, Assert
"""

from fastapi.testclient import TestClient
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