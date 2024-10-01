from fastapi import Depends, HTTPException, status
import logging

from app.util.mongo_singleton import MongoSingleton
from pymongo.database import Database
from app.domain.schemas.notes_schema import  NoteSchema
from app.domain.schemas.note_reponses_schema import *


# Create a new note
def create_note(note: NoteSchema, db: Database):
    # Function to get the next ID for an entity
    def get_next_id(collection_name: str):
        highest_entry =  db[collection_name].find_one({}, sort=[("id", -1)])  # Replace "id" with the field used for IDs in the collection
        return (highest_entry["id"] + 1) if highest_entry else 1  # Start from 1 if no entries

    # Check if the class exists; create if it does not
    existing_classe =  db.classes.find_one({"nom": note.idclasse.nom, "prof": note.idclasse.prof})
    if not existing_classe:
        # Create the new class with the next ID
        next_classe_id = get_next_id("classes")
        classe_data = {
            "id": next_classe_id,
            "nom": note.idclasse.nom,
            "prof": note.idclasse.prof,
        }
        db.classes.insert_one(classe_data)
        note.idclasse.id = next_classe_id  # Update the note with the new class ID
    else:
        note.idclasse = existing_classe  # Embed the existing class object

    # Check if the student exists; create if they do not
    existing_eleve = db.eleves.find_one({
        "nom": note.ideleve.nom,
        "prenom": note.ideleve.prenom,
        "date_naissance": note.ideleve.date_naissance
    })
    if not existing_eleve:
        # Create the new student with the next ID
        next_eleve_id = get_next_id("eleves")
        eleve_data = {
            "id": next_eleve_id,
            "nom": note.ideleve.nom,
            "prenom": note.ideleve.prenom,
            "classe": note.ideleve.classe,
            "date_naissance": note.ideleve.date_naissance,
            "adresse": note.ideleve.adresse,
            "sexe": note.ideleve.sexe,
        }
        db.eleves.insert_one(eleve_data)
        note.ideleve.id = next_eleve_id  # Update the note with the new student ID
    else:
        note.ideleve = existing_eleve  # Embed the existing student object

    # Check if the subject exists; create if it does not
    existing_matiere = db.matieres.find_one({"nom": note.idmatiere.nom})
    if not existing_matiere:
        # Create the new subject with the next ID
        next_matiere_id = get_next_id("matieres")
        matiere_data = {
            "id": next_matiere_id,
            "nom": note.idmatiere.nom,
        }
        db.matieres.insert_one(matiere_data)
        note.idmatiere.idmatiere = next_matiere_id  # Update the note with the new subject ID
    else:
        note.idmatiere = existing_matiere  # Embed the existing subject object

    # Check if the professor exists; create if they do not
    existing_prof = db.profs.find_one({
        "nom": note.idprof.nom,
        "prenom": note.idprof.prenom,
        "date_naissance": note.idprof.date_naissance
    })
    if not existing_prof:
        # Create the new professor with the next ID
        next_prof_id = get_next_id("profs")
        prof_data = {
            "id": next_prof_id,
            "nom": note.idprof.nom,
            "prenom": note.idprof.prenom,
            "date_naissance": note.idprof.date_naissance,
            "adresse": note.idprof.adresse,
            "sexe": note.idprof.sexe,
        }
        db.profs.insert_one(prof_data)
        note.idprof.id = next_prof_id  # Update the note with the new professor ID
    else:
        note.idprof = existing_prof  # Embed the existing professor object

    # Check if the trimester exists; create if it does not
    existing_trimestre = db.trimestres.find_one({"nom": note.idtrimestre.nom, "date": note.idtrimestre.date})
    if not existing_trimestre:
        # Create the new trimester with the next ID
        next_trimestre_id = get_next_id("trimestres")
        trimestre_data = {
            "id": next_trimestre_id,
            "nom": note.idtrimestre.nom,
            "date": note.idtrimestre.date,
        }
        db.trimestres.insert_one(trimestre_data)
        note.idtrimestre.idtrimestre = next_trimestre_id  # Update the note with the new trimester ID
    else:
        note.idtrimestre = existing_trimestre  # Embed the existing trimester object

    # Prepare the note data
    db_note = {
        "avancement": note.avancement,
        "avis": note.avis,
        "date_saisie": note.date_saisie,
        "idclasse": note.idclasse["id"],
        "ideleve": note.ideleve["id"],
        "idmatiere": note.idmatiere["idmatiere"],
        "idprof": note.idprof["id"],
        "idtrimestre": note.idtrimestre["idtrimestre"],
        "note": note.note,
        "idnotes": get_next_id("notes")
    }

    # Insert the note into the database
    result = db.notes.insert_one(db_note)

    # Return the newly created note
    return {"message": "Note added successfully", "_id": str(result.inserted_id)}


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