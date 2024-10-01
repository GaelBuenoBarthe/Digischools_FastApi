from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class ProfesseurBaseSchema(BaseModel):
    id: int
    nom: str
    prenom: str
    date_naissance: Optional[datetime] = Field(None, description="Date de naissance au format YYYY-MM-DD")
    adresse: Optional[str] = None
    sexe: Optional[str] = Field(None, description="Sexe du professeur")

    @field_validator('sexe')
    def validate_sexe(cls, v):
        if v not in ["HOMME", "FEMME"]:
            raise ValueError("sexe doit être 'HOMME' ou 'FEMME'")
        return v

    class Config:
        from_attributes = True

class ProfesseurCreateSchema(ProfesseurBaseSchema):
    pass

class ProfesseurUpdateSchema(BaseModel):
    nom: Optional[str]
    prenom: Optional[str]
    date_naissance: Optional[datetime] = Field(None, description="Date de naissance au format YYYY-MM-DD")
    adresse: Optional[str] = None
    sexe: Optional[str] = Field(None, description="Sexe du professeur")

    @field_validator('sexe')
    def validate_sexe(cls, v):
        if v not in ["HOMME", "FEMME"]:
            raise ValueError("sexe doit être 'HOMME' ou 'FEMME'")
        return v

    class Config:
        from_attributes = True

class ProfesseurResponseSchema(ProfesseurBaseSchema):
    pass