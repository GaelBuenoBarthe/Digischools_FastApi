from fastapi import Depends, HTTPException
from pymongo.database import Database
from app.util.mongo_singleton import MongoSingleton as get_db
from app.domain.schemas.matieres_schema import MatiereSchema

async def get_all_matieres(db: Database = Depends(get_db)):
    matieres = list(db.matieres.find(projection={"_id": False}))
    return matieres

async def get_matiere_by_id(idmatiere: int, db: Database = Depends(get_db)):
    matiere = db.matieres.find_one({"idmatiere": idmatiere}, projection={"_id": False})
    if matiere is None:
        raise HTTPException(status_code=404, detail="Matiere non trouvée")
    return matiere