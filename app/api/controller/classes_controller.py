import logging
from fastapi import Depends, HTTPException
from pymongo.database import Database
from app.domain.schemas.classes_schema import ClasseCreateUpdateSchema
from app.util.mongo_singleton import MongoSingleton

#Recupère toutes les classes
async def get_all_classes(db: Database = Depends(MongoSingleton.get_db)):
    classes = list(db.classes.find(projection={"_id": False}))
    return classes

#Recupère une classe par ID
async def get_classe_by_id(classe_id: int, db: Database = Depends(MongoSingleton.get_db)):
    classe = db.classes.find_one({"id": classe_id}, projection={"_id": False})
    if classe is None:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    return classe

# Creer une classe
async def create_class(classe: ClasseCreateUpdateSchema, db: Database = Depends(MongoSingleton.get_db)):
    logging.info(f"Vérification si une classe avec id  {classe.id} existe")
    existing_class = db.classes.find_one({"id": classe.id})
    if existing_class:
        logging.error(f"Classe avec id {classe.id} existe déja")
        raise HTTPException(status_code=400, detail="Classe avec cet ID existe déjà")

    logging.info(f"Creation d 'un classe avec id {classe.id}")
    db.classes.insert_one(classe.dict())
    return classe

# Modifier une classe
async def update_class(class_id: int, classe: ClasseCreateUpdateSchema, db: Database = Depends(MongoSingleton.get_db)):
    logging.info(f"modifier classe avec id {class_id}")
    result = db.classes.update_one({"id": class_id}, {"$set": classe.dict()})
    if result.matched_count == 0:
        logging.error(f"Classe avec id {class_id} not trouvée")
        raise HTTPException(status_code=404, detail="Classe non trouvée")

    updated_class = db.classes.find_one({"id": class_id}, projection={"_id": False})
    return updated_class

# Supprimer une classe
async def delete_class(class_id: int, db: Database = Depends(MongoSingleton.get_db)):
    result = db.classes.delete_one({"id": class_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Classe non trouvée")
    return {"message": "Classe supprimée avec succès"}