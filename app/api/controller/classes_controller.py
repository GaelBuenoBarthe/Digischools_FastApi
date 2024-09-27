from typing import List
from fastapi import Depends, HTTPException
from starlette import status

from app.domain.schemas import classes_schema
from app.util.mongo_singleton import get_db
from pymongo.database import Database

async def get_all_classes(db: Database = Depends(get_db)):
    classes = list(db.classes.find(projection={"_id": False}))
    return classes

async def get_classe_by_id(classe_id: int, db: Database = Depends(get_db)):
    classe = db.classes.find_one({"id": classe_id}, projection={"_id": False})
    if classe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classe non trouvée")
    return classe