from fastapi import APIRouter, Depends
from typing import List
from app.api.controller.eleves_controller import get_all_eleves, get_eleve_by_id, get_eleves_by_class, delete_eleve, \
    update_eleve, create_eleve
from app.domain.entities.eleves import Eleve
from app.domain.schemas.eleves_schema import EleveSchema
from pymongo.database import Database
from app.util.mongo_singleton import  MongoSingleton

router = APIRouter()

@router.get("/", response_model=List[EleveSchema])
async def read_all_eleves(db: Database = Depends(MongoSingleton.get_db)):
    return await get_all_eleves(db)

@router.post("/", response_model=Eleve)
async def create_eleve_endpoint(eleve: Eleve, db: Database = Depends(MongoSingleton.get_db)):
    return await create_eleve(eleve, db)

@router.put("/{eleve_id}", response_model=EleveSchema)
async def update_eleve_endpoint(eleve_id: int, eleve: EleveSchema, db: Database = Depends(MongoSingleton.get_db)):
    return await update_eleve(eleve_id, eleve, db)

@router.delete("/{eleve_id}", response_model=dict)
async def delete_eleve_endpoint(eleve_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await delete_eleve(eleve_id, db)

@router.get("/classe/{classe_id}", response_model=List[EleveSchema])
async def read_eleves_by_classe(classe_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await get_eleves_by_class(classe_id, db)

@router.get("/{eleve_id}", response_model=EleveSchema)
async def read_eleve_by_id(eleve_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await get_eleve_by_id(eleve_id, db)
