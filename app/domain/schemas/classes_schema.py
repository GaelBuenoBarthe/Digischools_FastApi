from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

# Schema pour la sous-collection Prof
class ProfSchema(BaseModel):
    id: int
    nom: str
    prenom: str
    date_naissance: datetime
    adresse: str
    sexe: str

    @field_validator('sexe')
    def validate_sexe(cls, v):
        if v not in ["HOMME", "FEMME"]:
            raise ValueError("sexe doit être 'HOMME' ou 'FEMME'")
        return v

# Schema pour l'entité Classe
class ClasseSchema(BaseModel):
    id: int
    nom: str
    prof: ProfSchema

    model_config = ConfigDict(from_attributes=True)