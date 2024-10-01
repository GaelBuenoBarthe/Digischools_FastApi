from typing import List

from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.api.controller.professeurs_controller import get_all_professeurs, get_professeur_by_id, create_professeur, \
    update_professeur, delete_professeur
from app.util.mongo_singleton import MongoSingleton
from app.domain.schemas.professeurs_response_schema import ProfesseurResponseSchema
from app.domain.schemas.professeur_update_schema import ProfesseurUpdateSchema
from app.domain.schemas.professeur_create_schema import ProfesseurCreateSchema

router = APIRouter()

@router.get("/", response_model=List[ProfesseurCreateSchema])
async def read_professeurs(db: Database = Depends(MongoSingleton.get_db)):
    return await get_all_professeurs(db)

@router.get("/{professeur_id}", response_model=ProfesseurCreateSchema)
async def read_professeur(professeur_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await get_professeur_by_id(professeur_id, db)

@router.post("/", response_model=ProfesseurResponseSchema)
async def create_professeur_endpoint(professeur: ProfesseurCreateSchema, db: Database = Depends(MongoSingleton.get_db)):
    from app.api.controller.professeurs_controller import create_professeur
    return await create_professeur(professeur, db)

@router.put("/{professeur_id}", response_model=ProfesseurResponseSchema)
async def update_professeur_endpoint(professeur_id: int, professeur: ProfesseurUpdateSchema, db: Database = Depends(MongoSingleton.get_db)):
    from app.api.controller.professeurs_controller import update_professeur
    return await update_professeur(professeur_id, professeur, db)

@router.delete("/{professeur_id}")
async def delete_professeur_endpoint(professeur_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await delete_professeur(professeur_id, db)
