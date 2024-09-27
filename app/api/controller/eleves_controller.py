from fastapi import Depends, HTTPException, status
from app.util.mongo_singleton import get_db
from pymongo.database import Database

async def get_all_eleves(db: Database = Depends(get_db)):
    eleves = list(db.eleves.find(projection={"_id": False}))
    return eleves

async def get_eleves_by_class(classe_id: int, db: Database = Depends(get_db)):
    eleves = list(db.eleves.find({"idclasse": classe_id}, projection={"_id": False}))
    if not eleves:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucun élève trouvé pour la classe avec l'ID {classe_id}")
    return eleves

async def get_eleve_by_id(eleve_id: int, db: Database = Depends(get_db)):
    eleve = db.eleves.find_one({"id": eleve_id}, projection={"_id": False})
    if eleve is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Élève non trouvé")
    return eleve