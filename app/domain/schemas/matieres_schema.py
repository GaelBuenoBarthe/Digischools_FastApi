from pydantic import BaseModel, Field

class MatiereSchema(BaseModel):
    idmatiere: int = Field(..., description="Identifiant unique pour matiere")
    nom: str

    class Config:
        from_attributes = True