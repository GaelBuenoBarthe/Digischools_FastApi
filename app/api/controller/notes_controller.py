from fastapi import Depends, HTTPException, status
from app.util.mongo_singleton import get_db
from pymongo.database import Database
from pymongo import UpdateOne
from app.domain.schemas import notes_schema as NoteSchema  # Assuming you have a schema for validation


# Create a new note
async def create_note(note: NoteSchema, db: Database = Depends(get_db)):
    existing_note = await db.notes.find_one({"idnotes": note.idnotes})
    if existing_note:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Note already exists.")

    result = await db.notes.insert_one(note.dict())
    return {"message": "Note added successfully", "id": str(result.inserted_id)}


# Get all notes
async def get_all_notes(db: Database = Depends(get_db)):
    notes = list(db.notes.find({}, projection={"_id": False}))
    return notes


# Update an existing note
async def update_note(idnotes: int, note: NoteSchema, db: Database = Depends(get_db)):
    result = await db.notes.update_one({"idnotes": idnotes}, {"$set": note.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")
    return {"message": "Note updated successfully."}


# Delete a note
async def delete_note(idnotes: int, db: Database = Depends(get_db)):
    result = await db.notes.delete_one({"idnotes": idnotes})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")
    return {"message": "Note deleted successfully."}


# Get notes by student
async def get_notes_by_eleve(eleve_id: int, db: Database = Depends(get_db)):
    notes = list(db.notes.find({"ideleve": eleve_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour l'élève avec l'ID {eleve_id}")
    return notes

# Get notes by teacher
async def get_notes_by_professeur(professeur_id: int, db: Database = Depends(get_db)):
    notes = list(db.notes.find({"idprof": professeur_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour le professeur avec l'ID {professeur_id}")
    return notes

# Get notes by class
async def get_notes_by_classe(classe_id: int, db: Database = Depends(get_db)):
    notes = list(db.notes.find({"idclasse": classe_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour la classe avec l'ID {classe_id}")
    return notes

# Get notes by trimester
async def get_notes_by_trimester(trimester_id: int, db: Database = Depends(get_db)):
    notes = list(db.notes.find({"idtrimestre": trimester_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour le trimestre avec l'ID {trimester_id}")
    return notes


async def get_notes_by_student_and_trimester(nom: str, trimester_id: int, db: Database = Depends(get_db)):
    notes = list(db.notes_by_student_and_trimester.find({"nom": nom, "idtrimestre": trimester_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour l'élève nommé {nom} et le trimestre {trimester_id}")
    return notes

async def get_notes_by_teacher_and_class(nom: str, professeur_id: int, db: Database = Depends(get_db)):
    notes = list(db.notes_by_teacher_and_class.find({"nom": nom, "idprof": professeur_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour le professeur avec l'ID {professeur_id} dans la classe {nom}")
    return notes


