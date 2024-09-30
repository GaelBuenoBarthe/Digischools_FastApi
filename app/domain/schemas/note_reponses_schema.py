from datetime import datetime
from pydantic import BaseModel
from typing import Any, List

class NoteDetail(BaseModel):
    eleve_id: int
    eleve_nom: str
    eleve_prenom: str
    matiere_nom: str
    trimestre_nom: str
    trimestre_start: datetime
    note: int

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import List

class NoteReponseProfClass(BaseModel):
    classe_nom: str
    classe_prof: int
    prof_nom: str
    prof_prenom: str
    notes: List[NoteDetail]
    classe_id: int
    prof_id: int

    class Config:
        from_attributes = True