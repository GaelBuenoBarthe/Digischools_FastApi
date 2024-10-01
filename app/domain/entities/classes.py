from pydantic import BaseModel, ConfigDict
from app.domain.schemas.classes_schema import ProfSchema

# Class pour la collection Classe
class Classe(BaseModel):
    id: int
    nom: str
    prof: ProfSchema

    model_config = ConfigDict(from_attributes=True)