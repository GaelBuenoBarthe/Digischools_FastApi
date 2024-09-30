from fastapi import APIRouter, Depends
from typing import List
from app.api.controller.matieres_controller import get_all_matieres, get_matiere_by_id
from app.domain.schemas import matieres_schema
from pymongo.database import Database
from app.util.mongo_singleton import MongoSingleton as get_db

router = APIRouter()

@router.get("/", response_model=List[matieres_schema])
async def read_matieres(db: Database = Depends(get_db)):
    return await get_all_matieres(db)

@router.get("/{matiere_id}", response_model=matieres_schema)
async def read_matiere(matiere_id: int, db: Database = Depends(get_db)):
    return await get_matiere_by_id(matiere_id, db)