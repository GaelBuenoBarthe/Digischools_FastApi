from fastapi import APIRouter, Path
from app.api.controller.notes_controller import *

from app.domain.schemas.notes.note_reponses_schema import NoteReponseProfClass
from app.domain.schemas.notes.note_reponse_stutri_schema import NoteReponseStuTri
from app.util.mongo_singleton import MongoSingleton
from app.domain.schemas.notes.notes_schema import NoteSchema
from app.domain.schemas.notes.notes_create_schema import NoteCreateSchema
from app.domain.schemas.notes.notes_update_schema import NoteUpdateSchema

router = APIRouter()

@router.get("/", response_model=list[NoteSchema])
async def read_all_notes(db: Database = Depends(MongoSingleton.get_db)):
    return await get_all_notes(db)


@router.post("/")
def create_note_endpoint(note: NoteCreateSchema, db: Database = Depends(MongoSingleton.get_db)):
    return create_note(note, db)

@router.put("/{note_id}", response_model=NoteUpdateSchema)
async def update_note_endpoint(note_id: int, note: NoteUpdateSchema, db: Database = Depends(MongoSingleton.get_db)):
    existing_note = db.notes.find_one({"idnotes": note_id})
    if not existing_note:
        raise HTTPException(status_code=404, detail="Note non trouvée")

    update_data = {"note": note.note}
    db.notes.update_one({"idnotes": note_id}, {"$set": update_data})

    updated_note = db.notes.find_one({"idnotes": note_id})
    return updated_note

@router.delete("/{note_id}")
async def delete_note_endpoint(note_id: int, db: Database = Depends(MongoSingleton.get_db)):
    return await delete_note(note_id, db)

@router.get("/eleve/{eleve_id}", response_model=list[NoteSchema])
async def read_notes_by_eleve(eleve_id: int = Path(..., title="The ID of the student"), db: Database = Depends(MongoSingleton.get_db)):
    return await get_notes_by_eleve( eleve_id, db)

@router.get("/trimestre/{trimester_id}", response_model=list[NoteSchema])
async def read_notes_by_trimester(trimester_id: int = Path(..., title="The ID of the trimester"), db: Database = Depends(MongoSingleton.get_db)):
    return await get_notes_by_trimester(trimester_id, db)

@router.get("/professeur/{professeur_id}", response_model=list[NoteSchema])
async def read_notes_by_prof(professeur_id: int = Path(..., title="The ID of the professeur"), db: Database = Depends(MongoSingleton.get_db)):
    return await get_notes_by_professeur(professeur_id, db)

@router.get("/eleve/{eleveid}/trimestre/{trimesterid}", response_model=list[NoteReponseStuTri])
async def read_notes_by_student_and_trimester(
    eleveid: int ,
    trimesterid: int ,
    db: Database = Depends(MongoSingleton.get_db)
):
    return await get_notes_by_student_and_trimester(eleveid, trimesterid, db)


@router.get("/professeur/{professeur_id}/classe/{classes_id}", response_model=NoteReponseProfClass)
async def read_notes_by_teacher_and_class(
    professeur_id: int = Path(..., title="L'ID du professeur"),
    classes_id: int = Path(..., title="L'ID de la classe"),
    db: Database = Depends(MongoSingleton.get_db)
):
    return await get_notes_by_teacher_and_class(classes_id, professeur_id, db)