from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime

# Schema pour la sous-collection Prof
class ClasseSchema(BaseModel):
    id: int
    nom: str
    prof: int

# Schema pour la collection Eleve
class EleveSchema(BaseModel):
    id: int
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

    model_config = ConfigDict(from_attributes=True)