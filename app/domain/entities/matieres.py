from app.domain.schemas import Matiere as MatiereSchema

class Matiere:
    def __init__(self, id: int, nom: str):
        self.id = id
        self.nom = nom

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom
        }

    @classmethod
    def from_schema(cls, schema: MatiereSchema):
        return cls(
            id=schema.id,
            nom=schema.nom
        )