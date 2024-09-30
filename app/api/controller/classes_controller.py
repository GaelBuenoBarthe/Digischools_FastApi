from fastapi import Depends, HTTPException
from pymongo.database import Database
from app.util.mongo_singleton import MongoSingleton

async def get_all_classes(db: Database = Depends(MongoSingleton.get_db)):
    classes = list(db.classes.find(projection={"_id": False}))
    return classes

async def get_classe_by_id(classe_id: int, db: Database = Depends(MongoSingleton.get_db)):
    classe = db.classes.find_one({"id": classe_id}, projection={"_id": False})
    if classe is None:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    return classe
