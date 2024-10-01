from fastapi import HTTPException
from pymongo.database import Database
from app.util.mongo_singleton import MongoSingleton
from app.domain.schemas.professeurs_schema import ProfesseurCreateSchema, ProfesseurUpdateSchema


# Fetch all professors
async def get_all_professeurs(db: Database):
    professeurs = list(db.professeurs.find(projection={"_id": False}))
    return professeurs


# Fetch professor by ID
async def get_professeur_by_id(professeur_id: int, db: Database):
    professeur = db.professeurs.find_one({"id": professeur_id}, projection={"_id": False})
    if not professeur:
        raise HTTPException(status_code=404, detail="Professeur not found")
    return professeur


# Create new professor
async def create_professeur(professeur: ProfesseurCreateSchema, db: Database):
    existing_professeur = db.professeurs.find_one({"id": professeur.id})

    if existing_professeur:
        raise HTTPException(status_code=400, detail="Professeur with this ID already exists")

    professeur_dict = professeur.dict()
    db.professeurs.insert_one(professeur_dict)
    return {"message": "Professeur created successfully", "professeur_id": professeur.id}


# Update professor by ID
async def update_professeur(professeur_id: int, professeur: ProfesseurUpdateSchema, db: Database):
    existing_professeur = db.professeurs.find_one({"id": professeur_id})

    if not existing_professeur:
        raise HTTPException(status_code=404, detail="Professeur not found")

    updated_data = {k: v for k, v in professeur.dict().items() if v is not None}  # Update only non-null fields
    db.professeurs.update_one({"id": professeur_id}, {"$set": updated_data})
    return {"message": "Professeur updated successfully"}


# Delete professor by ID
async def delete_professeur(professeur_id: int, db: Database):
    result = db.professeurs.delete_one({"id": professeur_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Professeur not found")

    return {"message": "Professeur deleted successfully"}
