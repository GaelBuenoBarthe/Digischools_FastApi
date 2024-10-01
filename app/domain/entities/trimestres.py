from app.domain.schemas import trimestres_schema as TrimestreSchema
from datetime import datetime

class Trimestre:
    def __init__(self, idtrimestre: int, nom: str, date: str | None = None):
        self.idtrimestre = idtrimestre
        self.nom = nom
        self.date = datetime

    def to_dict(self):
        return {
            "idtrimestre": self.idtrimestre,
            "nom": self.nom,
            "date": self.date
        }

    @classmethod
    def from_schema(cls, schema: TrimestreSchema):
        return cls(
            idtrimestre=schema.idtrimestre,
            nom=schema.nom,
            date=schema.date
        )