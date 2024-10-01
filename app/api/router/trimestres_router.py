from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.api.controller.trimestres_controller import get_all_trimestres, get_trimestre_by_id
from app.domain.schemas.trimestres_schema import TrimestreSchema
from pymongo.database import Database
from app.util.mongo_singleton import MongoSingleton

router = APIRouter()

@router.get("/", response_model=List[TrimestreSchema])
async def read_trimestres(db: Database = Depends(MongoSingleton.get_db)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    return await get_all_trimestres(db)

@router.get("/{trimestre_id}", response_model=TrimestreSchema)
async def read_trimestre(trimestre_id: int, db: Database = Depends(MongoSingleton.get_db)):
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    return await get_trimestre_by_id(trimestre_id, db)