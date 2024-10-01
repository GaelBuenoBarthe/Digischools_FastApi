from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.domain.schemas.matieres_schema import MatiereSchema
from app.api.controller.matieres_controller import get_all_matieres, get_matiere_by_id, update_matiere, create_matiere, \
    delete_matiere
from app.util.mongo_singleton import MongoSingleton
from pymongo.database import Database

router = APIRouter()

# Récupérer toutes les matières
@router.get("/", response_model=List[MatiereSchema])
async def read_all_matieres(db: Database = Depends(MongoSingleton.get_db)):
    return await get_all_matieres(db)

@router.get("/{matiere_id}", response_model=MatiereSchema)
async def read_matiere_by_id(matiere_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await get_matiere_by_id(matiere_id, db)

@router.post("/", response_model=MatiereSchema)
async def create_matiere_endpoint(matiere: MatiereSchema, db: Database = Depends(MongoSingleton.get_db)):
    return await create_matiere(matiere, db)

@router.put("/{matiere_id}", response_model=MatiereSchema)
async def update_matiere_endpoint(matiere_id: int, matiere: MatiereSchema, db: Database = Depends(MongoSingleton.get_db)):
    return await update_matiere(matiere_id, matiere, db)

@router.delete("/{matiere_id}", response_model=dict)
async def delete_matiere_endpoint(matiere_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await delete_matiere(matiere_id, db)