from app.domain.schemas import eleves_schema

class Eleve:
    def __init__(self, id: int, nom: str, prenom: str, idclasse: int, date_naissance: str | None = None, adresse: str | None = None, sexe: str | None = None):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.idclasse = idclasse
        self.date_naissance = date_naissance
        self.adresse = adresse
        self.sexe = sexe

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "idclasse": self.idclasse,
            "date_naissance": self.date_naissance,
            "adresse": self.adresse,
            "sexe": self.sexe
        }

    @classmethod
    def from_schema(cls, schema: eleves_schema):
        return cls(
            id=schema.id,
            nom=schema.nom,
            prenom=schema.prenom,
            idclasse=schema.idclasse,
            date_naissance=schema.date_naissance,
            adresse=schema.adresse,
            sexe=schema.sexe
        )