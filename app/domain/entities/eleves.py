from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

# Classe pour la sous-collection Classe
class Classe(BaseModel):
    id: int
    nom: str
    prof: int

# Classe pour la collection Eleve
class Eleve(BaseModel):
    id: int
    adresse: str
    classe: Classe
    date_naissance: datetime
    nom: str
    prenom: str
    sexe: str

    @field_validator('sexe')
    def validate_sexe(cls, v):
        if v not in ["HOMME", "FEMME"]:
            raise ValueError("sexe doit être 'HOMME' ou 'FEMME'")
        return v

    model_config = ConfigDict(from_attributes=True)