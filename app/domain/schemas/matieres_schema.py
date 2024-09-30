from pydantic import BaseModel

class MatiereSchema(BaseModel):
    idmatiere: int
    nom: str

    class Config:
        from_attributes = True