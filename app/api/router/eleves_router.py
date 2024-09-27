from fastapi import APIRouter, Depends
from typing import List
from app.api.controller.eleves_controller import get_all_eleves, get_eleves_by_class, get_eleve_by_id
from app.domain.schemas import eleves_schema
from pymongo.database import Database
from app.util.mongo_singleton import get_db

router = APIRouter()

@router.get("/", response_model=List[eleves_schema])
async def read_eleves(db: Database = Depends(get_db)):
    return await get_all_eleves(db)

@router.get("/{classe_id}", response_model=List[eleves_schema])
async def read_eleves_by_classe(classe_id: int, db: Database = Depends(get_db)):
    return await get_eleves_by_class(classe_id, db)

@router.get("/{eleve_id}", response_model=eleves_schema)
async def read_eleve(eleve_id: int, db: Database = Depends(get_db)):
    return await get_eleve_by_id(eleve_id, db)