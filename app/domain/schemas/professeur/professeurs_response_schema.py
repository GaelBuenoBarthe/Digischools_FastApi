from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProfesseurResponseSchema(BaseModel):
    id: int
    nom: str
    prenom: str
    date_naissance: Optional[datetime] = Field(None, description="Date de naissance au format YYYY-MM-DD")
    adresse: Optional[str] = None
    sexe: Optional[str] = Field(None, description="Sexe du professeur")

    class Config:
        from_attributes = True