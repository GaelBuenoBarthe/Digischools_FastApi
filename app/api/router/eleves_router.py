from fastapi import APIRouter, Depends
from typing import List
from app.api.controller.eleve_controller import get_all_eleves, get_eleves_by_class, get_eleve_by_id
from app.domain.schemas import Eleve
from pymongo.database import Database
from app.persistence.util import get_db

router = APIRouter()

@router.get("/", response_model=List[Eleve])
async def read_eleves(db: Database = Depends(get_db)):
    return await get_all_eleves(db)

@router.get("/{classe_id}", response_model=List[Eleve])
async def read_eleves_by_classe(classe_id: int, db: Database = Depends(get_db)):
    return await get_eleves_by_class(classe_id, db)

@router.get("/{eleve_id}", response_model=Eleve)
async def read_eleve(eleve_id: int, db: Database = Depends(get_db)):
    return await get_eleve_by_id(eleve_id, db)