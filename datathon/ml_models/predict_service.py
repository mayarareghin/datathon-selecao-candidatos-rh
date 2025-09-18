import joblib
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

df_vagas = pd.read_parquet("datathon/ml_models/vagas_preprocessed.parquet")
df_applicants = pd.read_parquet("datathon/ml_models/applicants_preprocessed.parquet")

modelo_rf = joblib.load("datathon/ml_models/modelo_supervisionado_rf.joblib")

modelo_sbert = SentenceTransformer("all-mpnet-base-v2")

_embeddings_cache_vagas = {}


def ranquear_top10_por_vaga(id_vaga: int):
     vaga = df_vagas[df_vagas['id_vaga'] == id_vaga]
     if vaga.empty:
        return {"erro": "Vaga não encontrada"}

     descricao = vaga.iloc[0]['perfil_vaga.principais_atividades']

     if id_vaga in _embeddings_cache_vagas:
        emb_vaga = _embeddings_cache_vagas[id_vaga]
     else:
        emb_vaga = modelo_sbert.encode(descricao)
        _embeddings_cache_vagas[id_vaga] = emb_vaga

     X_cv = np.stack(df_applicants['embedding_cv'].values)
     X_features = np.stack(df_applicants['features'].values)

     X_vaga = np.tile(emb_vaga, (X_cv.shape[0], 1))

     X_input = np.hstack([X_vaga, X_cv, X_features])

     probs = modelo_rf.predict_proba(X_input)[:, 1]

     df_resultados = pd.DataFrame({
        'id_candidato': df_applicants['id_candidato'],
        'nome': df_applicants.get('infos_basicas.nome', pd.Series([''] * len(df_applicants))),
        'probabilidade': np.round(probs, 4)
     })

     df_top10 = df_resultados.sort_values(by='probabilidade', ascending=False).head(10)

     return df_top10.to_dict(orient='records')
