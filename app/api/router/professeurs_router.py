from fastapi import APIRouter, Depends
from typing import List
from app.api.controller.professeur_controller import get_all_professeurs, get_professeur_by_id
from app.domain.schemas import Professeur
from pymongo.database import Database
from app.persistence.util import get_db

router = APIRouter()

@router.get("/", response_model=List[Professeur])
async def read_professeurs(db: Database = Depends(get_db)):
    return await get_all_professeurs(db)

@router.get("/{professeur_id}", response_model=Professeur)
async def read_professeur(professeur_id: int, db: Database = Depends(get_db)):
    return await get_professeur_by_id(professeur_id, db)