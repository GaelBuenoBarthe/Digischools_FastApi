from fastapi import Depends, HTTPException, status
from app.util.mongo_singleton import get_db
from pymongo.database import Database

async def get_notes_by_eleve(eleve_id: int, db: Database = Depends(get_db)):
    notes = list(db.notes.find({"ideleve": eleve_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour l'élève avec l'ID {eleve_id}")
    return notes

async def get_notes_by_professeur(professeur_id: int, db: Database = Depends(get_db)):
    notes = list(db.notes.find({"idprof": professeur_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour le professeur avec l'ID {professeur_id}")
    return notes

# ... autres fonctions pour récupérer les notes par classe, matière, trimestre, etc. (à implémenter selon vos besoins)