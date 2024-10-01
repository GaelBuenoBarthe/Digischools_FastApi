from http.client import HTTPException
from pymongo.database import Database
from app.domain.schemas.professeur.professeurs_response_schema import ProfesseurResponseSchema
from app.domain.schemas.professeur.professeur_update_schema import ProfesseurUpdateSchema
from app.domain.schemas.professeur.professeur_create_schema import ProfesseurCreateSchema


# Fetch all professors
async def get_all_professeurs(db: Database):
    professeurs = list(db.professeurs.find(projection={"_id": False}))
    return professeurs


# Fetch professor by ID
async def get_professeur_by_id(professeur_id: int, db: Database):
    professeur = db.professeurs.find_one({"id": professeur_id}, projection={"_id": False})
    if not professeur:
        raise HTTPException(status_code=404, detail="Professeur non trouvé")
    return professeur


# Creation d'un nouveau professeur
async def create_professeur(professeur: ProfesseurCreateSchema, db: Database) -> ProfesseurResponseSchema:
    existing_professeur = db.professeurs.find_one({"id": professeur.id})

    if existing_professeur:
        raise HTTPException(status_code=400, detail="Professeur avec cette ID existe déjà")

    professeur_dict = professeur.model_dump()
    db.professeurs.insert_one(professeur_dict)

    # Retourne le professeur créé
    return ProfesseurResponseSchema(**professeur_dict)


# Update professor by ID
async def update_professeur(professeur_id: int, professeur: ProfesseurUpdateSchema, db: Database) -> ProfesseurResponseSchema:
    existing_professeur = db.professeurs.find_one({"id": professeur_id})

    if not existing_professeur:
        raise HTTPException(status_code=404, detail="Professeur non trouvé")

    updated_data = {k: v for k, v in professeur.model_dump().items() if v is not None}
    db.professeurs.update_one({"id": professeur_id}, {"$set": updated_data})

    # Fetch the updated professor data
    updated_professeur = db.professeurs.find_one({"id": professeur_id}, projection={"_id": False})

    # Return the updated professor as a response
    return ProfesseurResponseSchema(**updated_professeur)


# Delete professor by ID
async def delete_professeur(professeur_id: int, db: Database):
    result = db.professeurs.delete_one({"id": professeur_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Professeur non trouvé")

    return {"message": "Professeur supprimer avec succés"}
