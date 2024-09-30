from fastapi import Depends, HTTPException
from starlette import status
from app.util.mongo_singleton import MongoSingleton as get_db
from pymongo.database import Database

async def get_all_trimestres(db: Database = Depends(get_db)):
    trimestres = list(db.trimestres.find(projection={"_id": False}))
    return trimestres

async def get_trimestre_by_id(trimestre_id: int, db: Database = Depends(get_db)):
    trimestre = db.trimestres.find_one({"idtrimestre": trimestre_id}, projection={"_id": False})
    if trimestre is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trimestre non trouvé")
    return trimestre