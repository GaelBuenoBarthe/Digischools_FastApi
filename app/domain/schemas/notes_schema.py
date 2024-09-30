from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


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


class NoteReponse1(BaseModel):
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

class NoteReponse2(BaseModel):
    note: int
    date_saisie: datetime
    avis : str
    avancement: str
    idclasse: ClasseSchema
    ideleve: EleveSchema
    idprof: ProfSchema
    idnotes: int


    class Config:
        arbitrary_types_allowed = True
