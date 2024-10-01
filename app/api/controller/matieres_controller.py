import logging

from fastapi import Depends, HTTPException
from pymongo.database import Database
from app.util.mongo_singleton import MongoSingleton
from app.domain.schemas.matieres_schema import MatiereSchema


#Récuperer toutes les matieres
async def get_all_matieres(db: Database = Depends(MongoSingleton.get_db)):
    matieres = list(db.matieres.find(projection={"_id": False}))
    return matieres

#Récuperer une matiere par ID
async def get_matiere_by_id(idmatiere: int, db: Database = Depends(MongoSingleton.get_db)):
    matiere = db.matieres.find_one({"idmatiere": idmatiere}, projection={"_id": False})
    if matiere is None:
        raise HTTPException(status_code=404, detail="Matiere non trouvée")
    return matiere

# Créer une matiere
async def create_matiere(matiere: MatiereSchema, db: Database = Depends(MongoSingleton.get_db)):
    logging.info(f"Verification que la matière avec l 'id {matiere.idmatiere} existe")
    existing_matiere = db.matieres.find_one({"idmatiere": matiere.idmatiere})
    if existing_matiere:
        logging.error(f"Matiere avec id {matiere.idmatiere} existe déja")
        raise HTTPException(status_code=400, detail="Matiere avec cet ID existe déjà")

    logging.info(f"Creation d'une matière avec ID {matiere.idmatiere}")
    db.matieres.insert_one(matiere.dict())
    return matiere

# Modifier une matiere
async def update_matiere(matiere_id: int, matiere: MatiereSchema, db: Database = Depends(MongoSingleton.get_db)):
    logging.info(f"Modification de la matiere avec ID {matiere_id}")
    result = db.matieres.update_one({"idmatiere": matiere_id}, {"$set": matiere.dict()})
    if result.matched_count == 0:
        logging.error(f"Matiere avec id {matiere_id} non trouvé")
        raise HTTPException(status_code=404, detail="Matiere non trouvée")

    updated_matiere = db.matieres.find_one({"idmatiere": matiere_id}, projection={"_id": False})
    return updated_matiere

# Supprimer une matiere
async def delete_matiere(matiere_id: int, db: Database = Depends(MongoSingleton.get_db)):
    result = db.matieres.delete_one({"idmatiere": matiere_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Matiere non trouvée")
    return {"message": "Matiere supprimée avec succès"}