from fastapi import Depends, HTTPException, status
from app.util.mongo_singleton import MongoSingleton
from pymongo.database import Database
from app.domain.schemas import notes_schema as NoteSchema


# Create a new note
async def create_note(note: NoteSchema, db: Database = Depends(MongoSingleton)):
    existing_note = await db.notes.find_one({"idnotes": note.idnotes})
    if existing_note:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Note already exists.")

    result = await db.notes.insert_one(note.dict())
    return {"message": "Note added successfully", "id": str(result.inserted_id)}


# Get all notes
from pymongo.database import Database
from app.domain.schemas.notes_schema import NoteSchema

async def get_all_notes(db: Database):
    notes = list(db.notes.find({}, projection={"_id": False}))
    return notes


# Update an existing note
async def update_note(idnotes: int, note: NoteSchema, db: Database = Depends(MongoSingleton)):
    result = await db.notes.update_one({"idnotes": idnotes}, {"$set": note.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")
    return {"message": "Note updated successfully."}


# Delete a note
async def delete_note(idnotes: int, db: Database = Depends(MongoSingleton)):
    result = await db.notes.delete_one({"idnotes": idnotes})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")
    return {"message": "Note deleted successfully."}


# Get notes by student
async def get_notes_by_eleve(eleve_id: int, db: Database = Depends(MongoSingleton)):
    notes = list(db.notes.find({"ideleve": eleve_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour l'élève avec l'ID {eleve_id}")
    return notes

# Get notes by teacher
async def get_notes_by_professeur(professeur_id: int, db: Database = Depends(MongoSingleton)):
    notes = list(db.notes.find({"idprof": professeur_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour le professeur avec l'ID {professeur_id}")
    return notes

# Get notes by class
async def get_notes_by_classe(classe_id: int, db: Database = Depends(MongoSingleton)):
    notes = list(db.notes.find({"idclasse": classe_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour la classe avec l'ID {classe_id}")
    return notes

# Get notes by trimester
async def get_notes_by_trimester(trimester_id: int, db: Database = Depends(MongoSingleton)):
    notes = list(db.notes.find({"idtrimestre": trimester_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour le trimestre avec l'ID {trimester_id}")
    return notes


async def get_notes_by_student_and_trimester(nom: str, trimester_id: int, db: Database = Depends(MongoSingleton)):
    notes = list(db.notes_by_student_and_trimester.find({"nom": nom, "idtrimestre": trimester_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour l'élève nommé {nom} et le trimestre {trimester_id}")
    return notes

async def get_notes_by_teacher_and_class(nom: str, professeur_id: int, db: Database = Depends(MongoSingleton)):
    notes = list(db.notes_by_teacher_and_class.find({"nom": nom, "idprof": professeur_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour le professeur avec l'ID {professeur_id} dans la classe {nom}")
    return notes

async def get_all_notes_by_eleve(db: Database, eleve_id: int):
    pipeline = [
        {
            "$match": {
                "ideleve.id": eleve_id
            }
        },
        {
            "$lookup": {
                "from": "eleve",
                "localField": "ideleve.id",
                "foreignField": "id",
                "as": "eleve_details"
            }
        },
        {
            "$unwind": "$eleve_details"
        },
        {
            "$project": {
                "_id": 0,
                "idnotes": 1,
                "avancement": 1,
                "avis": 1,
                "date_saisie": 1,
                "idclasse": 1,
                "ideleve": 1,
                "idmatiere": 1,
                "idprof": 1,
                "idtrimestre": 1,
                "note": 1,
                "eleve_details.nom": 1,
                "eleve_details.prenom": 1
            }
        }
    ]
    notes = list(db.notes.aggregate(pipeline))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour l'élève avec l'ID {eleve_id}")
    return notes
