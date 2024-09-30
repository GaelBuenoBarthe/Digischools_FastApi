from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from app.domain.schemas.notes_schema import NoteSchema


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

class NoteReponseStuTri(BaseModel):
    eleve_nom: str
    eleve_prenom: str
    classe: int
    trimestre_nom: str
    trimestre_start: datetime
    notes: List[int]  # Changed to List[int] for proper array handling
    average_note: float
    eleve_id: int  # Added field for student ID
    trimestre_id: int  # Added field for trimester ID

    class Config:
        arbitrary_types_allowed = True


class Note2Schema(BaseModel):
    eleve_id: int
    eleve_nom: str
    eleve_prenom: str
    matiere_Nom: str
    trimestre_start: datetime
    note: int


class NoteReponseReponseProfClass(BaseModel):
    classnom: str
    classprof: int
    profnom : str
    profprenom: str
    notes: List[Note2Schema]
    classe_id: int
    prof_id: int