from http import HTTPStatus
from typing import Annotated
from pathlib import Path
import pandas as pd

from fastapi import APIRouter, Depends, HTTPException

from datathon.db.models import User
from datathon.dependencies.security import get_current_user
from datathon.ml_models.predict_service import ranquear_top10_por_vaga

router = APIRouter(prefix="/predict", tags=["predict"])

CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/vaga/{id_vaga}")
async def predict_top10(id_vaga: int, current_user: CurrentUser):
    resultados = ranquear_top10_por_vaga(id_vaga)

    if resultados is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Vaga com ID {id_vaga} não encontrada."
        )

    if resultados == []:
        return {"message": f"Descrição da vaga {id_vaga} está vazia."}

    return {"vaga_id": id_vaga, "top10": resultados}

DATA_PATH = Path(__file__).resolve().parents[2] / "datathon" / "ml_models" / "vagas_preprocessed.parquet"

try:
    df_vagas = pd.read_parquet(DATA_PATH)
except Exception as e:
    raise RuntimeError(f"Erro ao carregar {DATA_PATH}: {e}")

@router.get("/buscar_vaga/{id_vaga}")
async def buscar_vaga(id_vaga: int, current_user: CurrentUser):
    """
    Retorna todas as informações da vaga com base no ID fornecido.
    """
    vaga = df_vagas[df_vagas["id_vaga"] == id_vaga]

    if vaga.empty:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")

    # Converte para dict (linha única -> dict normal)
    return vaga.iloc[0].to_dict()

CANDIDATOS_PATH = Path(__file__).resolve().parents[1] / "ml_models" / "applicants_preprocessed.parquet"

@router.get("/buscar_candidato/{id_candidato}")
async def buscar_candidato(id_candidato: int, current_user: CurrentUser):
    """Retorna informações completas de um candidato pelo ID, sem embeddings"""
    try:
        df = pd.read_parquet(CANDIDATOS_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dataset: {e}")

    candidato = df[df["id_candidato"] == id_candidato]
    if candidato.empty:
        raise HTTPException(status_code=404, detail="Candidato não encontrado")

    result = candidato.iloc[0].to_dict()

    # Remove colunas de embeddings ou arrays pesados
    for col in list(result.keys()):
        if "embedding" in col.lower() or isinstance(result[col], (list, dict)):
            del result[col]

    # Converte para tipos nativos simples (int, float, str)
    for k, v in result.items():
        if hasattr(v, "item"):  # numpy scalar
            try:
                result[k] = v.item()
            except Exception:
                result[k] = str(v)
        elif hasattr(v, "isoformat"):  # datetime
            result[k] = v.isoformat()

    return result