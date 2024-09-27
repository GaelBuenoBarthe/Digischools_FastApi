from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from app.util.mongo_singleton import get_db
from pymongo.database import Database
from app.domain.entities.classes import Classe

router = APIRouter()

# Récupérer toutes les classes
@router.get("/classes", response_model=list[Classe])
async def get_all_classes(db: Database = Depends(get_db)):
    classes = list(db.classes.find(projection={"_id": False}))
    return classes

# Récupérer une classe par ID
@router.get("/classes/{classe_id}", response_model=Classe)
async def get_classe_by_id(classe_id: int, db: Database = Depends(get_db)):
    classe = db.classes.find_one({"id": classe_id}, projection={"_id": False})
    if classe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classe non trouvée")
    return classe

# Créer une classe
@router.post("/classes", response_model=Classe)
async def create_classe(classe: Classe, db: Database = Depends(get_db)):
    if db.classes.find_one({"id": classe.id}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Classe déjà existante")
    db.classes.insert_one(classe.model_dump())
    return {"message": "Classe crée avec succès"}

# Mettre à jour une classe
@router.put("/classes/{classe_id}", response_model=Classe)
async def update_classe(classe_id: int, updated_classe: Classe, db: Database = Depends(get_db)):
    result = db.classes.update_one({"id": classe_id}, {"$set": updated_classe.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classe non trouvée")
    return {"message": "Classe modifiée avec succès"}

# Supprimer une classe
@router.delete("/classes/{classe_id}", response_model=dict)
async def delete_classe(classe_id: int, db: Database = Depends(get_db)):
    result = db.classes.delete_one({"id": classe_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classe non trouvée")
    return {"message": "Classe supprimée avec succès"}