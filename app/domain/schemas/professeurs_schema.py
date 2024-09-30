from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProfesseurSchema(BaseModel):
    id: int
    nom: str
    prenom: str
    date_naissance: datetime
    adresse: str
    sexe: str
    matiere: Optional[str] = Field(None, description="La matière enseignée par le professeur")

    class Config:
        from_attributes = True