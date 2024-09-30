from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.api.controller.professeurs_controller import get_all_professeurs, get_professeur_by_id
from app.domain.schemas.professeurs_schema import ProfesseurSchema
from pymongo.database import Database
from app.util.mongo_singleton import MongoSingleton

router = APIRouter()

@router.get("/", response_model=List[ProfesseurSchema])
async def read_professeurs(db: Database = Depends(MongoSingleton.get_db)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    return await get_all_professeurs(db)

@router.get("/{professeur_id}", response_model=ProfesseurSchema)
async def read_professeur(professeur_id: int, db: Database = Depends(MongoSingleton.get_db)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    return await get_professeur_by_id(professeur_id, db)