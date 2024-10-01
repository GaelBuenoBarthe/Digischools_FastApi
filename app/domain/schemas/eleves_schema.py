from pydantic import BaseModel, Field, validator, ConfigDict, field_validator
from datetime import datetime

class ClasseSchema(BaseModel):
    id: int
    nom: str
    prof: int

class EleveSchema(BaseModel):
    id: int = Field(..., description="Unique identifier for the eleve")
    adresse: str
    classe: ClasseSchema
    date_naissance: datetime
    nom: str
    prenom: str
    sexe: str

    @field_validator('sexe')
    def validate_sexe(cls, v):
        if v not in ["HOMME", "FEMME"]:
            raise ValueError("sexe doit être 'HOMME' ou 'FEMME'")
        return v

    class Config:
        from_attributes = True