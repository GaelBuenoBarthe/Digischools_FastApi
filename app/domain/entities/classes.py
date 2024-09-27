from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime

# Class pour la sous-collection Prof
class Prof(BaseModel):
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

# Classe pour l'entité Classe
class Classe(BaseModel):
    id: int
    nom: str
    prof: Prof

    model_config = ConfigDict(from_attributes=True)