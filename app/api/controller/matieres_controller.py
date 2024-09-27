from fastapi import Depends, HTTPException
from starlette import status
from app.util.mongo_singleton import MongoSingleton as get_db
from pymongo.database import Database

async def get_all_matieres(db: Database = Depends(get_db)):
    matieres = list(db.matieres.find(projection={"_id": False}))
    return matieres

async def get_matiere_by_id(matiere_id: int, db: Database = Depends(get_db)):
    matiere = db.matieres.find_one({"id": matiere_id}, projection={"_id": False})
    if matiere is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matière non trouvée")
    return matiere