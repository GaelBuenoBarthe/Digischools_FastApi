from datetime import datetime
from bson import ObjectId
from app.domain.schemas.notes import notes_schema as NoteSchema


class Note:
    def __init__(self, idnotes: int, ideleve: ObjectId, idclasse: ObjectId, idmatiere: ObjectId, idprof: ObjectId, idtrimestre: ObjectId, note: int, date_saisie: datetime | None = None, avis: str | None = None, avancement: float | None = None):
        self.idnotes = idnotes
        self.ideleve = ideleve
        self.idclasse = idclasse
        self.idmatiere = idmatiere
        self.idprof = idprof
        self.idtrimestre = idtrimestre
        self.note = note
        self.date_saisie = date_saisie
        self.avis = avis
        self.avancement = avancement

    def to_dict(self):
        return {
            "idnotes": self.idnotes,
            "ideleve": self.ideleve,
            "idclasse": self.idclasse,
            "idmatiere": self.idmatiere,
            "idprof": self.idprof,
            "idtrimestre": self.idtrimestre,
            "note": self.note,
            "date_saisie": self.date_saisie.isoformat() if self.date_saisie else None,  # Convert to ISO format for JSON serialization
            "avis": self.avis,
            "avancement": self.avancement
        }

    @classmethod
    def from_schema(cls, schema: NoteSchema):
        return cls(
            idnotes=schema.idnotes,
            ideleve=schema.ideleve,
            idclasse=schema.idclasse,
            idmatiere=schema.idmatiere,
            idprof=schema.idprof,
            idtrimestre=schema.idtrimestre,
            note=schema.note,
            date_saisie=schema.date_saisie,  # Ensure this is a datetime object
            avis=schema.avis,
            avancement=schema.avancement
        )
