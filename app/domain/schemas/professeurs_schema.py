from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProfesseurBaseSchema(BaseModel):
    id: int
    nom: str
    prenom: str
    date_naissance: Optional[datetime] = Field(None, description="Date of birth in YYYY-MM-DD format")
    adresse: Optional[str] = None
    sexe: Optional[str] = Field(None, description="Gender of the professor")

    class Config:
        orm_mode = True
        from_attributes = True


class ProfesseurCreateSchema(ProfesseurBaseSchema):
    pass


class ProfesseurUpdateSchema(BaseModel):
    nom: Optional[str]
    prenom: Optional[str]
    date_naissance: Optional[datetime] = Field(None, description="Date of birth in YYYY-MM-DD format")
    adresse: Optional[str] = None
    sexe: Optional[str] = Field(None, description="Gender of the professor")

    class Config:
        orm_mode = True
        from_attributes = True
