from typing import List

from fastapi import APIRouter, Depends
from pymongo.database import Database


from app.api.controller.professeurs_controller import *

from app.domain.schemas.professeurs_schema import ProfesseurCreateSchema, ProfesseurUpdateSchema
from app.util.mongo_singleton import MongoSingleton

router = APIRouter()

@router.get("/", response_model=List[ProfesseurCreateSchema])
async def read_professeurs(db: Database = Depends(MongoSingleton.get_db)):
    return await get_all_professeurs(db)

@router.get("/{professeur_id}", response_model=ProfesseurCreateSchema)
async def read_professeur(professeur_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await get_professeur_by_id(professeur_id, db)

@router.post("/", response_model=ProfesseurCreateSchema)
async def create_professeur_endpoint(professeur: ProfesseurCreateSchema, db: Database = Depends(MongoSingleton.get_db)):
    return await create_professeur(professeur, db)

@router.put("/{professeur_id}", response_model=ProfesseurCreateSchema)
async def update_professeur_endpoint(professeur_id: int, professeur: ProfesseurUpdateSchema, db: Database = Depends(MongoSingleton.get_db)):
    return await update_professeur(professeur_id, professeur, db)

@router.delete("/{professeur_id}")
async def delete_professeur_endpoint(professeur_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await delete_professeur(professeur_id, db)
