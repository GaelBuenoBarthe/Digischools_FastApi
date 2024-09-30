from fastapi import Depends, HTTPException, status
from app.util.mongo_singleton import MongoSingleton as get_db
from pymongo.database import Database

async def get_all_professeurs(db: Database = Depends(get_db)):
    professeurs = list(db.professeurs.find(projection={"_id": False}))
    return professeurs

async def get_professeur_by_id(professeur_id: int, db: Database = Depends(get_db)):
    professeur = db.professeurs.find_one({"id": professeur_id}, projection={"_id": False})
    if professeur is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professeur non trouvé")
    return professeur