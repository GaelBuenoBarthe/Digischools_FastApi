from fastapi import APIRouter, Depends
from typing import List
from app.api.controller.trimestres_controller import get_all_trimestres, get_trimestre_by_id
from app.domain.schemas import trimestres_schema
from pymongo.database import Database
from app.util.mongo_singleton import MongoSingleton as get_db

router = APIRouter()

@router.get("/", response_model=List[trimestres_schema])
async def read_trimestres(db: Database = Depends(get_db)):
    return await get_all_trimestres(db)

@router.get("/{trimestre_id}", response_model=trimestres_schema)
async def read_trimestre(trimestre_id: int, db: Database = Depends(get_db)):
    return await get_trimestre_by_id(trimestre_id, db)