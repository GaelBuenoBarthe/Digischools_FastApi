from fastapi import HTTPException
from app.util.mongo_singleton import MongoSingleton


async def get_all_professeurs(db):
    professeurs = list(db.professeurs.find(projection={"_id": False}))
    return professeurs

async def get_professeur_by_id(professeur_id: int, db):
    professeur = db.professeurs.find_one({"id": professeur_id}, projection={"_id": False})
    if not professeur:
        raise HTTPException(status_code=404, detail="Professeur not found")
    return professeur