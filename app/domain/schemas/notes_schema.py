from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from bson import ObjectId

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
    avis: str | None = None
    date_saisie: datetime
    idclasse: ClasseSchema
    ideleve: EleveSchema
    idmatiere: MatiereSchema
    idprof: ProfSchema
    idtrimestre: TrimestreSchema
    note: int

    model_config = ConfigDict(arbitrary_types_allowed=True)