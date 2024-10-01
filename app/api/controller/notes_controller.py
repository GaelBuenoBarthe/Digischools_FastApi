from fastapi import Depends, HTTPException, status
import logging
from app.util.mongo_singleton import MongoSingleton
from pymongo.database import Database
from app.domain.schemas.notes.notes_schema import  NoteSchema
from app.domain.schemas.notes.note_reponses_schema import *
from fastapi import HTTPException
from pymongo.database import Database
from app.domain.schemas.notes.notes_create_schema import NoteCreateSchema
from app.domain.schemas.notes.notes_update_schema import NoteUpdateSchema

# Creation d'une nouvelle note
def create_note(note: NoteCreateSchema, db: Database):
    # Fonction pour obtenir le prochain ID pour une entité
    def get_next_id(collection_name: str):
        highest_entry = db[collection_name].find_one({}, sort=[("id", -1)])  # Remplacer "id" par le champ utilisé pour les IDs dans la collection
        if highest_entry and "id" in highest_entry:
            return highest_entry["id"] + 1
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Impossible de déterminer le prochain ID")

    # Vérifier si la classe existe ; créer si elle n'existe pas
    existing_classe = db.classes.find_one({"id": note.idclasse.id})
    if not existing_classe:
        next_classe_id = note.idclasse.id if note.idclasse.id else get_next_id("classes")
        classe_data = {
            "id": next_classe_id,
            "nom": note.idclasse.nom,
            "prof": note.idclasse.prof,
        }
        db.classes.insert_one(classe_data)
        note.idclasse.id = next_classe_id  # Mettre à jour la note avec le nouvel ID de la classe
    else:
        note.idclasse.id = existing_classe["id"]  # Intégrer l'ID de la classe existante

    # Vérifier si l'élève existe ; créer s'il n'existe pas
    existing_eleve = db.eleves.find_one({"id": note.ideleve.id})
    if not existing_eleve:
        next_eleve_id = note.ideleve.id if note.ideleve.id else get_next_id("eleves")
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
        note.ideleve.id = next_eleve_id  # Mettre à jour la note avec le nouvel ID de l'élève
    else:
        note.ideleve.id = existing_eleve["id"]  # Intégrer l'ID de l'élève existant

    # Vérifier si la matière existe ; créer si elle n'existe pas
    existing_matiere = db.matieres.find_one({"idmatiere": note.idmatiere.idmatiere})
    if not existing_matiere:
        next_matiere_id = note.idmatiere.idmatiere if note.idmatiere.idmatiere else get_next_id("matieres")
        matiere_data = {
            "idmatiere": next_matiere_id,
            "nom": note.idmatiere.nom,
        }
        db.matieres.insert_one(matiere_data)
        note.idmatiere.idmatiere = next_matiere_id  # Mettre à jour la note avec le nouvel ID de la matière
    else:
        note.idmatiere.idmatiere = existing_matiere["idmatiere"]  # Intégrer l'ID de la matière existante

    # Vérifier si le professeur existe ; créer s'il n'existe pas
    existing_prof = db.professeurs.find_one({"id": note.idprof.id})
    if not existing_prof:
        next_prof_id = note.idprof.id if note.idprof.id else get_next_id("professeurs")
        prof_data = {
            "id": next_prof_id,
            "nom": note.idprof.nom,
            "prenom": note.idprof.prenom,
            "date_naissance": note.idprof.date_naissance,
            "adresse": note.idprof.adresse,
            "sexe": note.idprof.sexe,
        }
        db.professeurs.insert_one(prof_data)
        note.idprof.id = next_prof_id  # Mettre à jour la note avec le nouvel ID du professeur
    else:
        note.idprof.id = existing_prof["id"]  # Intégrer l'ID du professeur existant

    # Vérifier si le trimestre existe ; créer s'il n'existe pas
    existing_trimestre = db.trimestres.find_one({"idtrimestre": note.idtrimestre.idtrimestre})
    if not existing_trimestre:
        next_trimestre_id = note.idtrimestre.idtrimestre if note.idtrimestre.idtrimestre else get_next_id("trimestres")
        trimestre_data = {
            "idtrimestre": next_trimestre_id,
            "nom": note.idtrimestre.nom,
            "date": note.idtrimestre.date,
        }
        db.trimestres.insert_one(trimestre_data)
        note.idtrimestre.idtrimestre = next_trimestre_id  # Mettre à jour la note avec le nouvel ID du trimestre
    else:
        note.idtrimestre.idtrimestre = existing_trimestre["idtrimestre"]  # Intégrer l'ID du trimestre existant

    # Préparer les données de la note
    db_note = {
        "idnotes": note.idnotes if note.idnotes else get_next_id("notes"),
        "avancement": note.avancement,
        "avis": note.avis,
        "date_saisie": note.date_saisie,
        "idclasse": note.idclasse.dict(),
        "ideleve": note.ideleve.dict(),
        "idmatiere": note.idmatiere.dict(),
        "idprof": note.idprof.dict(),
        "idtrimestre": note.idtrimestre.dict(),
        "note": note.note,
    }

    # Insérer la note dans la base de données
    result = db.notes.insert_one(db_note)

    # Retourner la note nouvellement créée
    return {"message": "Note ajoutée avec succès", "_id": str(result.inserted_id)}

# Get all notes
async def get_all_notes(db: Database):
    notes = list(db.notes.find({}, projection={"_id": False}))
    return notes


# Update an existing note
async def update_note(idnotes: int, note: NoteUpdateSchema, db: Database = Depends(MongoSingleton)):
    result = await db.notes.update_one({"idnotes": idnotes}, {"$set": note.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")
    return {"message": "Note updated successfully."}


# Delete a note
async def delete_note(idnotes, db):
    result = db.notes.delete_one({"idnotes": idnotes})
    if result.deleted_count == 1:
        return {"message": "Note supprimée avec succès"}
    else:
        return {"message": "Note non trouvée"}


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