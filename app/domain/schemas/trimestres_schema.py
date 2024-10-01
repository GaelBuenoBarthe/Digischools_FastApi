from pydantic import BaseModel
from datetime import datetime

class TrimestreSchema(BaseModel):
    idtrimestre: int
    nom: str
    date: datetime

    class Config:
        from_attributes = True