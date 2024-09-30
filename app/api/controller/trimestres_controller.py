from fastapi import Depends, HTTPException
from starlette import status
from app.util.mongo_singleton import MongoSingleton
from pymongo.database import Database

async def get_all_trimestres(db):
    trimestres = list(db.trimestres.find(projection={"_id": False}))
    return trimestres

async def get_trimestre_by_id(trimestre_id: int, db: Database = Depends(MongoSingleton.get_db())):
    trimestre = db.trimestres.find_one({"idtrimestre": trimestre_id}, projection={"_id": False})
    if trimestre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trimestre non trouvé")
    return trimestre