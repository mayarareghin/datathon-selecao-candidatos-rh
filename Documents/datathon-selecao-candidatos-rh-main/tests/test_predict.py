from http import HTTPStatus
from unittest.mock import patch
import pytest
import pandas as pd
from pathlib import Path

# TESTES DO /predict/vaga
def test_predict_success(client_with_auth):
    mock_result = [
        {"id_candidato": 1, "nome": "Alice", "probabilidade": 0.95},
        {"id_candidato": 2, "nome": "Bob", "probabilidade": 0.90}, 
    ]

    with patch("datathon.routers.predict.ranquear_top10_por_vaga", return_value=mock_result):
        response = client_with_auth.get("/predict/vaga/123")

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert "top10" in data
    assert isinstance(data["top10"], list)
    
    for cand, expected in zip(data["top10"], mock_result):
        for key in expected:
            assert cand[key] == expected[key]


def test_predict_vaga_not_found(client_with_auth):
    with patch("datathon.routers.predict.ranquear_top10_por_vaga", return_value=None):
        response = client_with_auth.get("/predict/vaga/999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Vaga com ID 999 não encontrada."


def test_predict_sem_token(client):
    # Client sem autenticação
    response = client.get("/predict/vaga/123")

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


# TESTES DO /predict/buscar_vaga 
DATA_PATH = Path(__file__).resolve().parents[1] / "datathon" / "ml_models" / "vagas_preprocessed.parquet"

def test_buscar_vaga_success(client_with_auth):
    # Carrega dataset real para pegar um ID válido
    df = pd.read_parquet(DATA_PATH)
    id_existente = int(df.iloc[0]["id_vaga"])

    response = client_with_auth.get(f"/predict/buscar_vaga/{id_existente}")

    assert response.status_code == HTTPStatus.OK
    vaga = response.json()

    assert vaga["id_vaga"] == id_existente
    assert len(vaga.keys()) > 1


def test_buscar_vaga_not_found(client_with_auth):
    response = client_with_auth.get("/predict/buscar_vaga/999999999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Vaga não encontrada"


# TESTES DO /predict/buscar_candidato 
def test_buscar_candidato_sucesso(client_with_auth):
    mock_candidato = {
        "id_candidato": 1,
        "nome": "Alice",
        "idade": 29,
        "experiencia": "Cientista de Dados",
    }

    with patch("datathon.routers.predict.pd.read_parquet") as mock_read:
        mock_df = pd.DataFrame([mock_candidato])
        mock_read.return_value = mock_df

        response = client_with_auth.get("/predict/buscar_candidato/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == mock_candidato


def test_buscar_candidato_nao_encontrado(client_with_auth):
    with patch("datathon.routers.predict.pd.read_parquet") as mock_read:
        mock_df = pd.DataFrame(columns=["id_candidato", "nome", "idade", "experiencia"])
        mock_read.return_value = mock_df

        response = client_with_auth.get("/predict/buscar_candidato/999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Candidato não encontrado"


def test_buscar_candidato_erro_leitura(client_with_auth):
    with patch("datathon.routers.predict.pd.read_parquet", side_effect=Exception("Falha no dataset")):
        response = client_with_auth.get("/predict/buscar_candidato/1")

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert "Erro ao carregar dataset" in response.json()["detail"]