from fastapi import APIRouter

from app.api.controller.notes_controller import create_note, get_all_notes, get_notes_by_eleve, get_notes_by_professeur, \
    get_notes_by_classe, get_notes_by_trimester, update_note, delete_note, get_notes_by_teacher_and_class, \
    get_notes_by_student_and_trimester
from app.util.mongo_singleton import get_db
from app.domain.schemas.notes_schema import NoteSchema

router = APIRouter()

@router.post("/notes/", response_model=dict)
async def add_note(note: NoteSchema):
    return await create_note(note)

@router.get("/notes/", response_model=list)
async def read_all_notes():
    return await get_all_notes()

@router.get("/notes/elevé/{eleve_id}", response_model=list)
async def read_notes_by_eleve(eleve_id: int):
    return await get_notes_by_eleve(eleve_id)

@router.get("/notes/professeur/{professeur_id}", response_model=list)
async def read_notes_by_professeur(professeur_id: int):
    return await get_notes_by_professeur(professeur_id)

@router.get("/notes/classe/{classe_id}", response_model=list)
async def read_notes_by_classe(classe_id: int):
    return await get_notes_by_classe(classe_id)

@router.get("/notes/trimestre/{trimester_id}", response_model=list)
async def read_notes_by_trimester(trimester_id: int):
    return await get_notes_by_trimester(trimester_id)

@router.put("/notes/{idnotes}", response_model=dict)
async def modify_note(idnotes: int, note: NoteSchema):
    return await update_note(idnotes, note)

@router.delete("/notes/{idnotes}", response_model=dict)
async def remove_note(idnotes: int):
    return await delete_note(idnotes)
@router.get("/notes/professeur/{professeur_id}/classe/{classe_id}", response_model=list)
async def read_notes_by_teacher_and_class(professeur_id: int, classe_id: int):
    return await get_notes_by_teacher_and_class(professeur_id, classe_id)

@router.get("/notes/elevé/{eleve_id}/trimestre/{trimester_id}", response_model=list)
async def read_notes_by_student_and_trimester(eleve_id: int, trimester_id: int):
    return await get_notes_by_student_and_trimester(eleve_id, trimester_id)
