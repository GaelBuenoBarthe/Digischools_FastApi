from pydantic import BaseModel

class Matiere(BaseModel):
    idmatiere: int
    nom: str