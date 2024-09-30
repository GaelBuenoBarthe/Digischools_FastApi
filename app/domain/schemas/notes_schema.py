from pydantic import BaseModel, Field
from typing import Any

class ClassModel(BaseModel):
    id: int
    nom: str
    prof: int

class StudentModel(BaseModel):
    id: int
    nom: str
    prenom: str
    classe: int
    date_naissance: Any
    adresse: str
    sexe: str

class ProfModel(BaseModel):
    id: int
    nom: str
    prenom: str
    date_naissance: Any
    adresse: str
    sexe: str

class NoteSchema(BaseModel):
    note: int
    date_saisie: Any
    avis: str
    avancement: str
    class_: ClassModel = Field(..., alias='class')
    student: StudentModel
    prof: ProfModel
    idnotes: int
    idclasse: int
    ideleve: int
    idprof: int

    class Config:
        populate_by_name = True

class NoteReponse1(BaseModel):
    note: int
    avis: str
    avancement: str
    idnotes: int
    idclasse: int
    ideleve: int
    idprof: int

class NoteReponse2(BaseModel):
    note: int
    date_saisie: Any
    avis: str
    avancement: str
    idnotes: int
    idclasse: int
    ideleve: int
    idprof: int