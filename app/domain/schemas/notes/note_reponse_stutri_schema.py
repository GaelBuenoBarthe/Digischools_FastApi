from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class NoteReponseStuTri(BaseModel):
    eleve_nom: str
    eleve_prenom: str
    classe: int
    trimestre_nom: str
    trimestre_start: datetime
    notes: List[int]
    average_note: float
    eleve_id: int
    trimestre_id: int

    class Config:
        from_attributes = True