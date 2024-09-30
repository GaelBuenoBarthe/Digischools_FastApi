from fastapi import Depends, HTTPException, status
import logging

from app.util.mongo_singleton import MongoSingleton
from pymongo.database import Database
from app.domain.schemas.notes_schema import  NoteSchema
from app.domain.schemas.note_reponses_schema import *


# Create a new note
async def create_note(note: NoteSchema, db: Database = Depends(MongoSingleton)):
    existing_note = await db.notes.find_one({"idnotes": note.idnotes})
    if existing_note:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Note already exists.")

    result = await db.notes.insert_one(note.dict())
    return {"message": "Note added successfully", "id": str(result.inserted_id)}


# Get all notes


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
    notes = list(db.notes.find({"ideleve.id": eleve_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour l'élève avec l'ID {eleve_id}")
    return notes

# Get notes by teacher
async def get_notes_by_professeur(professeur_id: int, db: Database = Depends(MongoSingleton)):
    notes = list(db.notes.find({"idprof.id": professeur_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour le professeur avec l'ID {professeur_id}")
    return notes


# Get notes by class
async def get_notes_by_classe(classe_id: int, db: Database = Depends(MongoSingleton)):
    notes = list(db.notes.find({"idclasse.id": classe_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour la classe avec l'ID {classe_id}")
    return notes


# Get notes by trimester
async def get_notes_by_trimester(trimester_id: int, db: Database = Depends(MongoSingleton)):
    notes = list(db.notes.find({"idtrimestre.idtrimestre": trimester_id}, projection={"_id": False}))
    if not notes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Aucune note trouvée pour le trimestre avec l'ID {trimester_id}")
    return notes

#Getnotes by Student and trimester

async def get_notes_by_student_and_trimester(
        eleveid: int,
        trimesterid: int,
        db: Database = Depends(MongoSingleton.get_db)
):
    # Query the view directly by student ID and trimester ID
    query = {
        "eleve_id": eleveid,  # Filter by student ID
        "trimestre_id": trimesterid  # Filter by trimester ID
    }

    # Query the MongoDB view that has the aggregation logic implemented
    results = list(db.view_stu_tri.find(query))

    # Handle case where no results are found
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pas de notes pour l'élève avec l'ID {eleveid} au trimestre {trimesterid}"
        )

    # Return the retrieved results
    return results

#Recuperer les notes par professeur et classe
async def get_notes_by_teacher_and_class(classes_id: int, professeur_id: int, db: Database):
    try:
        notes = list(db.view_teacher_lecture.find({"classe_id": classes_id, "prof_id": professeur_id}, projection={"_id": False}))
        if not notes:
            raise HTTPException(status_code=404, detail="Aucunes notes trouvées pour cette classe et ce professeur")

        note_details = [
            NoteDetail(
                eleve_id=note['eleve_id'],
                eleve_nom=note['eleve_nom'],
                eleve_prenom=note['eleve_prenom'],
                matiere_nom=note['matiere_nom'],
                trimestre_nom=note['trimestre_nom'],
                trimestre_start=note['trimestre_start'],
                note=note['note']
            )
            for note in notes[0]['notes']
        ]

        return NoteReponseProfClass(
            classe_nom=notes[0]['classe_nom'],
            classe_prof=notes[0]['classe_prof'],
            prof_nom=notes[0]['prof_nom'],
            prof_prenom=notes[0]['prof_prenom'],
            notes=note_details,
            classe_id=notes[0]['classe_id'],
            prof_id=notes[0]['prof_id']
        )
    except KeyError as e:
        logging.error(f"KeyError: {e} - Check the structure of the note")
        raise HTTPException(status_code=500, detail=f"KeyError: {e} - Verifier la structure de note")