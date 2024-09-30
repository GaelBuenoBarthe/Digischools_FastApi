import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.domain.schemas.eleves_schema import EleveSchema
from app.util.mongo_singleton import MongoSingleton
from pymongo.database import Database
from app.domain.entities.eleves import Eleve

router = APIRouter()

# Récupérer tous les élèves
@router.get("/eleves", response_model=list[Eleve])
async def get_all_eleves(db: Database = Depends(MongoSingleton.get_db)):
    eleves = list(db.eleves.find(projection={"_id": False}))
    return eleves

# Récupérer un élève par ID
@router.get("/eleves/{eleve_id}", response_model=Eleve)
async def get_eleve_by_id(eleve_id: int, db: Database = Depends(MongoSingleton.get_db)):
    eleve = db.eleves.find_one({"id": eleve_id}, projection={"_id": False})
    if eleve is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève non trouvé")
    return eleve

# Récupérer les élèves par ID de la classe
@router.get("/eleves/classe/{classe_id}", response_model=List[Eleve])
async def get_eleves_by_class(classe_id: int, db: Database = Depends(MongoSingleton.get_db)):
    eleves = list(db.eleves.find({"classe.id": classe_id}, projection={"_id": False}))
    if not eleves:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun élève trouvé pour cette classe")
    return eleves

# Créer un élève
async def create_eleve(eleve: EleveSchema, db: Database = Depends(MongoSingleton.get_db)):
    logging.info(f"Checking if eleve with id {eleve.id} exists")
    existing_eleve = db.eleves.find_one({"id": eleve.id})
    if existing_eleve:
        logging.error(f"Élève with id {eleve.id} already exists")
        raise HTTPException(status_code=400, detail="Élève déjà existant")

    logging.info(f"Inserting eleve with id {eleve.id}")
    db.eleves.insert_one(eleve.model_dump())
    return eleve

# Mettre à jour un élève
@router.put("/eleves/{eleve_id}", response_model=Eleve)
async def update_eleve(eleve_id: int, updated_eleve: Eleve, db: Database = Depends(MongoSingleton.get_db)):
    result = db.eleves.update_one({"id": eleve_id}, {"$set": updated_eleve.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève non trouvé")
    return {"message": "Élève modifié avec succès"}

# Supprimer un élève
@router.delete("/eleves/{eleve_id}", response_model=dict)
async def delete_eleve(eleve_id: int, db: Database = Depends(MongoSingleton.get_db)):
    result = db.eleves.delete_one({"id": eleve_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève non trouvé")
    return {"message": "Élève supprimé avec succès"}