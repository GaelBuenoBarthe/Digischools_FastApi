from fastapi import APIRouter, Depends, Path
from pymongo.database import Database
from app.api.controller.notes_controller import get_all_notes, get_all_notes_by_eleve, get_notes_by_trimester, get_notes_by_student_and_trimester, get_notes_by_teacher_and_class
from app.util.mongo_singleton import MongoSingleton
from app.domain.schemas.notes_schema import NoteSchema

router = APIRouter()

@router.get("/notes/", response_model=list[NoteSchema])
async def read_all_notes(db: Database = Depends(MongoSingleton.get_db)):
    return await get_all_notes(db)

@router.get("/notes/elevé/{eleve_id}", response_model=list[NoteSchema])
async def read_notes_by_eleve(eleve_id: int = Path(..., title="The ID of the student"), db: Database = Depends(MongoSingleton.get_db)):
    return await get_all_notes_by_eleve(db, eleve_id)

@router.get("/notes/trimestre/{trimester_id}", response_model=list[NoteSchema])
async def read_notes_by_trimester(trimester_id: int = Path(..., title="The ID of the trimester"), db: Database = Depends(MongoSingleton.get_db)):
    return await get_notes_by_trimester(trimester_id, db)

@router.get("/notes/elevé/{eleve_id}/trimestre/{trimester_id}", response_model=list[NoteSchema])
async def read_notes_by_student_and_trimester(eleve_id: int = Path(..., title="The ID of the student"), trimester_id: int = Path(..., title="The ID of the trimester"), db: Database = Depends(MongoSingleton.get_db)):
    return await get_notes_by_student_and_trimester(eleve_id, trimester_id, db)

@router.get("/notes/professeur/{professeur_id}/classe/{classe_id}", response_model=list[NoteSchema])
async def read_notes_by_teacher_and_class(professeur_id: int = Path(..., title="The ID of the teacher"), classe_id: int = Path(..., title="The ID of the class"), db: Database = Depends(MongoSingleton.get_db)):
    return await get_notes_by_teacher_and_class(professeur_id, classe_id, db)