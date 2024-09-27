from fastapi import APIRouter, Depends
from typing import List
from app.api.controller.notes_controller import get_notes_by_eleve, get_notes_by_professeur
from app.domain.schemas import notes_schema
from pymongo.database import Database
from app.util.mongo_singleton import get_db

router = APIRouter()

@router.get("/eleve/{eleve_id}", response_model=List[notes_schema])
async def read_notes_by_eleve(eleve_id: int, db: Database = Depends(get_db)):
    return await get_notes_by_eleve(eleve_id, db)

@router.get("/professeur/{professeur_id}", response_model=List[notes_schema])
async def read_notes_by_professeur(professeur_id: int, db: Database = Depends(get_db)):
    return await get_notes_by_professeur(professeur_id, db)
