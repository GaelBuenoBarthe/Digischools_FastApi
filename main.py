from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.api.router.classes_router import router as classes_router
from app.api.router.eleves_router import router as eleves_router

#Créer une instance de FastAPI
app = FastAPI()

# Route pour les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Route pour la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Inclure les routeurs
app.include_router(classes_router, prefix="/classes", tags=["classes"])
app.include_router(eleves_router, prefix="/eleves", tags=["eleves"])

# Exécuter l'application avec Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)