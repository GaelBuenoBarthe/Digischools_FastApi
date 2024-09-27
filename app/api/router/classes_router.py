from fastapi import APIRouter, Depends
from typing import List
from app.api.controller.classe_controller import get_all_classes, get_classe_by_id
from app.domain.schemas import Classe
from pymongo.database import Database
from app.persistence.util import get_db

router = APIRouter()

@router.get("/", response_model=List[Classe])
async def read_classes(db: Database = Depends(get_db)):
    return await get_all_classes(db)

@router.get("/{classe_id}", response_model=Classe)
async def read_classe(classe_id: int, db: Database = Depends(get_db)):
    return await get_classe_by_id(classe_id, db)