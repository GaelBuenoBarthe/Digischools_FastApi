from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from app.util.mongo_singleton import get_db
from pymongo.database import Database
from app.domain.entities.eleves import Eleve

router = APIRouter()

# Récupérer tous les élèves
@router.get("/eleves", response_model=list[Eleve])
async def get_all_eleves(db: Database = Depends(get_db)):
    eleves = list(db.eleves.find(projection={"_id": False}))
    return eleves

# Récupérer un élève par ID
@router.get("/eleves/{eleve_id}", response_model=Eleve)
async def get_eleve_by_id(eleve_id: int, db: Database = Depends(get_db)):
    eleve = db.eleves.find_one({"id": eleve_id}, projection={"_id": False})
    if eleve is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève non trouvé")
    return eleve

# Récupérer les élèves par ID de la classe
@router.get("/eleves/classe/{classe_id}", response_model=List[Eleve])
async def get_eleves_by_class(classe_id: int, db: Database = Depends(get_db)):
    eleves = list(db.eleves.find({"classe.id": classe_id}, projection={"_id": False}))
    if not eleves:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun élève trouvé pour cette classe")
    return eleves

# Créer un élève
@router.post("/eleves", response_model=Eleve)
async def create_eleve(eleve: Eleve, db: Database = Depends(get_db)):
    if db.eleves.find_one({"id": eleve.id}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Élève déjà existant")
    db.eleves.insert_one(eleve.model_dump())
    return {"message": "Élève créé avec succès"}

# Mettre à jour un élève
@router.put("/eleves/{eleve_id}", response_model=Eleve)
async def update_eleve(eleve_id: int, updated_eleve: Eleve, db: Database = Depends(get_db)):
    result = db.eleves.update_one({"id": eleve_id}, {"$set": updated_eleve.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève non trouvé")
    return {"message": "Élève modifié avec succès"}

# Supprimer un élève
@router.delete("/eleves/{eleve_id}", response_model=dict)
async def delete_eleve(eleve_id: int, db: Database = Depends(get_db)):
    result = db.eleves.delete_one({"id": eleve_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève non trouvé")
    return {"message": "Élève supprimé avec succès"}