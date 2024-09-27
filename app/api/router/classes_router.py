from fastapi import APIRouter, Depends
from typing import List
from app.api.controller.classes_controller import get_all_classes, get_classe_by_id
from app.domain.schemas import classes_schema
from pymongo.database import Database
from app.util.mongo_singleton import MongoSingleton as get_db

router = APIRouter()

@router.get("/", response_model=List[classes_schema])
async def read_classes(db: Database = Depends(get_db)):
    return await get_all_classes(db)

@router.get("/{classe_id}", response_model=classes_schema)
async def read_classe(classe_id: int, db: Database = Depends(get_db)):
    return await get_classe_by_id(classe_id, db)