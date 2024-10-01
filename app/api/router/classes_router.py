from fastapi import APIRouter, Depends
from typing import List
from pymongo.database import Database
from app.domain.entities.classes import Classe
from app.api.controller.classes_controller import get_all_classes, get_classe_by_id, update_class, delete_class, \
    create_class
from app.domain.schemas.classes_schema import ClasseSchema, ClasseCreateUpdateSchema
from app.util.mongo_singleton import MongoSingleton

router = APIRouter()
# Récupérer toutes les classes
@router.get("/", response_model=List[Classe])
async def read_all_classes(db: Database = Depends(MongoSingleton.get_db)):
    return await get_all_classes(db)

# Récupérer une classe par ID
@router.get("/{classe_id}", response_model=Classe)
async def read_classe(classe_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await get_classe_by_id(classe_id, db)

# Créer une classe
@router.post("/", response_model=ClasseSchema)
async def create_class_endpoint(classe: ClasseCreateUpdateSchema, db: Database = Depends(MongoSingleton.get_db)):
    return await create_class(classe, db)

# Modifier une classe
@router.put("/{class_id}", response_model=ClasseSchema)
async def update_class_endpoint(class_id: int, classe: ClasseCreateUpdateSchema, db: Database = Depends(MongoSingleton.get_db)):
    return await update_class(class_id, classe, db)

# Supprimer une classe
@router.delete("/{class_id}", response_model=dict)
async def delete_class_endpoint(class_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await delete_class(class_id, db)
