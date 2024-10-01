from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class ClasseSchema(BaseModel):
    id: Optional[int]
    nom: str
    prof: int

class EleveSchema(BaseModel):
    id: Optional[int]
    nom: str
    prenom: str
    classe: int
    date_naissance: datetime
    adresse: str
    sexe: str

class MatiereSchema(BaseModel):
    idmatiere: Optional[int]
    nom: str

class ProfSchema(BaseModel):
    id: Optional[int]
    nom: str
    prenom: str
    date_naissance: datetime
    adresse: str
    sexe: str

class TrimestreSchema(BaseModel):
    idtrimestre: Optional[int]
    nom: str
    date: datetime

class NoteCreateSchema(BaseModel):
    idnotes: Optional[int]
    avancement: int
    avis: str
    date_saisie: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Date de la note")
    idclasse: ClasseSchema
    ideleve: EleveSchema
    idmatiere: MatiereSchema
    idprof: ProfSchema
    idtrimestre: TrimestreSchema
    note: float

    class Config:
        from_attributes = True