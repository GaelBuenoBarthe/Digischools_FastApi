from app.domain.schemas import Professeur as ProfesseurSchema

class Professeur:
    def __init__(self, id: int, nom: str, prenom: str, date_naissance: str | None = None, adresse: str | None = None, sexe: str | None = None):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.adresse = adresse
        self.sexe = sexe

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance,
            "adresse": self.adresse,
            "sexe": self.sexe
        }

    @classmethod
    def from_schema(cls, schema: ProfesseurSchema):
        return cls(
            id=schema.id,
            nom=schema.nom,
            prenom=schema.prenom,
            date_naissance=schema.date_naissance,
            adresse=schema.adresse,
            sexe=schema.sexe
        )