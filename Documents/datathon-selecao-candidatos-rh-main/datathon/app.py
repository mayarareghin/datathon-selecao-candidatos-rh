# datathon/app.py

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from datathon.routers import auth, predict, users
from datathon.core.logging_config import setup_logging # <--- ADIÇÃO 1: IMPORTAR A CONFIGURAÇÃO

app = FastAPI(title='Seleção de candidatos')

# <--- ADIÇÃO 2: ADICIONAR O BLOCO DE STARTUP AQUI
@app.on_event("startup")
def startup_event():
    """
    Função executada quando a aplicação inicia para ativar o logging.
    """
    setup_logging()

app.include_router(predict.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
async def redirect_to_docs():
    return RedirectResponse(url='/docs', status_code=302)