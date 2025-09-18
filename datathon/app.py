from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from datathon.routers import auth, predict, users


app = FastAPI(title='Seleção de candidatos')

app.include_router(predict.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
async def redirect_to_docs():
    return RedirectResponse(url='/docs', status_code=302)
