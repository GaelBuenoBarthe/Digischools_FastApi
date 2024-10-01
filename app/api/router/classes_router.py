from fastapi import APIRouter, Depends
from typing import List
from pymongo.database import Database
from app.domain.entities.classes import Classe
from app.api.controller.classes_controller import get_all_classes, get_classe_by_id
from app.util.mongo_singleton import MongoSingleton

router = APIRouter()

@router.get("/", response_model=List[Classe])
async def read_all_classes(db: Database = Depends(MongoSingleton.get_db)):
    return await get_all_classes(db)

@router.get("/{classe_id}", response_model=Classe)
async def read_classe(classe_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await get_classe_by_id(classe_id, db)
