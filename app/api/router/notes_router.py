from fastapi import APIRouter, Depends
from typing import List
from app.api.controller.note_controller import get_notes_by_eleve, get_notes_by_professeur
from app.domain.schemas import Note
from pymongo.database import Database
from app.persistence.util import get_db

router = APIRouter()

@router.get("/eleve/{eleve_id}", response_model=List[Note])
async def read_notes_by_eleve(eleve_id: int, db: Database = Depends(get_db)):
    return await get_notes_by_eleve(eleve_id, db)

@router.get("/professeur/{professeur_id}", response_model=List[Note])
async def read_notes_by_professeur(professeur_id: int, db: Database = Depends(get_db)):
    return await get_notes_by_professeur(professeur_id, db)

# ... autres routes pour récupérer les notes par classe, matière, trimestre, etc. (à implémenter selon vos besoins)