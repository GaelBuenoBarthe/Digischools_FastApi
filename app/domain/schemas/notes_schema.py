from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId

class NoteSchema(BaseModel):
    idnotes: int
    eleve_id: ObjectId  # Reference to the `eleves` collection
    classe_id: ObjectId  # Reference to the `classes` collection
    matiere_id: ObjectId  # Reference to the `matieres` collection
    prof_id: ObjectId  # Reference to the `profs` collection
    trimestre_id: ObjectId  # Reference to the `trimestres` collection
    note: int
    date_saisie: datetime  # Using datetime for date
    avis: str | None = None
    avancement: float | None = None

    class Config:
        # Allow MongoDB ObjectId serialization
        json_encoders = {
            ObjectId: str
        }
