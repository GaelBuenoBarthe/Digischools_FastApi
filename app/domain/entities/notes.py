from app.domain.schemas import notes_schema as NoteSchema

class Note:
    def __init__(self, idnotes: int, ideleve: int, idclasse: int, idmatiere: int, idprof: int, idtrimestre: int, note: int, date_saisie: str | None = None, avis: str | None = None, avancement: float | None = None):
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
            "date_saisie": self.date_saisie,
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
            date_saisie=schema.date_saisie,
            avis=schema.avis,
            avancement=schema.avancement
        )