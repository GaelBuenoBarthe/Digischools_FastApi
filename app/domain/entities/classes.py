from pydantic import BaseModel, field_validator, ConfigDict
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from app.domain.schemas.classes_schema import ClasseSchema, ProfSchema

# Class pour la collection Classe
class Classe(BaseModel):
    id: int
    nom: str
    prof: ProfSchema

    model_config = ConfigDict(from_attributes=True)