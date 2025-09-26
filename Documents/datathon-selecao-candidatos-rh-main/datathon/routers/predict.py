# predict.py (versão com logs)

from http import HTTPStatus
from typing import Annotated
from pathlib import Path
import pandas as pd
import logging # <--- ADIÇÃO 1: IMPORTAR O LOGGING

from fastapi import APIRouter, Depends, HTTPException

from datathon.db.models import User
from datathon.dependencies.security import get_current_user
from datathon.ml_models.predict_service import ranquear_top10_por_vaga

# <--- ADIÇÃO 2: PEGAR UMA INSTÂNCIA DO LOGGER
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/predict", tags=["predict"])

CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get("/vaga/{id_vaga}")
async def predict_top10(id_vaga: int, current_user: CurrentUser):
    
    # <--- ADIÇÃO 3: LOG INICIAL DA REQUISIÇÃO
    logger.info(
        "Requisição de predição recebida", 
        extra={"vaga_id": id_vaga, "usuario": current_user.username}
    )
    
    try:
        resultados = ranquear_top10_por_vaga(id_vaga)

        if resultados is None:
            # Log para o caso de a vaga não ser encontrada
            logger.warning(
                "Vaga não encontrada durante a predição", 
                extra={"vaga_id": id_vaga}
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Vaga com ID {id_vaga} não encontrada."
            )

        if resultados == []:
            # Log para o caso de a descrição da vaga estar vazia
            logger.info(
                "Predição não pôde ser gerada (descrição da vaga vazia)",
                extra={"vaga_id": id_vaga}
            )
            return {"message": f"Descrição da vaga {id_vaga} está vazia."}

        # <--- ADIÇÃO 4: LOG DETALHADO PARA ANÁLISE DE DRIFT
        # Este é o log mais importante para o monitoramento do modelo.
        for candidato in resultados:
            logger.info(
                "Predição de candidato gerada",
                extra={
                    "vaga_id": id_vaga,
                    "candidato_id": candidato.get('id_candidato'),
                    "probabilidade_predita": candidato.get('probabilidade'),
                }
            )

        return {"vaga_id": id_vaga, "top10": resultados}

    except Exception as e:
        # <--- ADIÇÃO 5: LOG DE ERRO GENÉRICO
        # Captura qualquer outra exceção que possa ocorrer.
        logger.error(
            f"Falha inesperada ao processar predição para vaga_id: {id_vaga}",
            exc_info=True # Adiciona o traceback completo do erro ao log
        )
        raise HTTPException(
            status_code=500, detail='Ocorreu um erro interno ao processar a predição.'
        )

# O restante do arquivo continua igual...
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

    for col in list(result.keys()):
        if "embedding" in col.lower() or isinstance(result[col], (list, dict)):
            del result[col]

    for k, v in result.items():
        if hasattr(v, "item"):
            try:
                result[k] = v.item()
            except Exception:
                result[k] = str(v)
        elif hasattr(v, "isoformat"):
            result[k] = v.isoformat()

    return result