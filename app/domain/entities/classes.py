from app.domain.schemas import classes_schema as ClasseSchema

class Classe:
    def __init__(self, id: int, nom: str, prof: int):
        self.id = id
        self.nom = nom
        self.prof = prof

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prof": self.prof
        }

    @classmethod
    def from_schema(cls, schema: ClasseSchema):
        return cls(
            id=schema.id,
            nom=schema.nom,
            prof=schema.prof
        )