from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.api.router.classes_router import router as classes_router
from app.api.router.eleves_router import router as eleves_router
from app.api.router.notes_router import router as notes_router
from app.api.router.matieres_router import router as matieres_router

app = FastAPI()

# Route pour les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Route pour la page d'accueil
app.include_router(notes_router, prefix="/notes", tags=["Notes"])
app.include_router(matieres_router, prefix="/matieres", tags=["Matieres"])

# Inclure les routeurs
app.include_router(classes_router, prefix="/classes", tags=["classes"])
app.include_router(eleves_router, prefix="/eleves", tags=["eleves"])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


