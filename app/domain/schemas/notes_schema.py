from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ClasseSchema(BaseModel):
    id: int
    nom: str
    prof: int

class EleveSchema(BaseModel):
    id: int
    nom: str
    prenom: str
    classe: int
    date_naissance: datetime
    adresse: str
    sexe: str

class MatiereSchema(BaseModel):
    idmatiere: int
    nom: str

class ProfSchema(BaseModel):
    id: int
    nom: str
    prenom: str
    date_naissance: datetime
    adresse: str
    sexe: str

class TrimestreSchema(BaseModel):
    idtrimestre: int
    nom: str
    date: datetime

class NoteSchema(BaseModel):
    idnotes: int
    avancement: float
    avis: Optional[str] = None
    date_saisie: datetime
    idclasse: ClasseSchema
    ideleve: EleveSchema
    idmatiere: MatiereSchema
    idprof: ProfSchema
    idtrimestre: TrimestreSchema
    note: int

    class Config:
        arbitrary_types_allowed = True