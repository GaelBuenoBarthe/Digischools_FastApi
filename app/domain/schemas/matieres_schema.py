from pydantic import BaseModel

class MatiereSchema(BaseModel):
    idmatiere: int
    nom: str

    class Config:
        orm_mode = True