from fastapi import APIRouter, Depends, Path
from pymongo.database import Database
from app.api.controller.notes_controller import get_all_notes, get_notes_by_eleve, get_notes_by_trimester, \
    get_notes_by_student_and_trimester, get_notes_by_teacher_and_class, get_notes_by_professeur
from app.util.mongo_singleton import MongoSingleton
from app.domain.schemas.notes_schema import NoteSchema, NoteReponse1, NoteReponse2

router = APIRouter()

@router.get("/", response_model=list[NoteSchema])
async def read_all_notes(db: Database = Depends(MongoSingleton.get_db)):
    return await get_all_notes(db)

@router.get("/eleve/{eleve_id}", response_model=list[NoteSchema])
async def read_notes_by_eleve(eleve_id: int = Path(..., title="The ID of the student"), db: Database = Depends(MongoSingleton.get_db)):
    return await get_notes_by_eleve( eleve_id, db)

@router.get("/trimestre/{trimester_id}", response_model=list[NoteSchema])
async def read_notes_by_trimester(trimester_id: int = Path(..., title="The ID of the trimester"), db: Database = Depends(MongoSingleton.get_db)):
    return await get_notes_by_trimester(trimester_id, db)

@router.get("/professeur/{professeur_id}", response_model=list[NoteSchema])
async def read_notes_by_prof(professeur_id: int = Path(..., title="The ID of the professeur"), db: Database = Depends(MongoSingleton.get_db)):
    return await get_notes_by_professeur(professeur_id, db)

@router.get("/eleve/{eleveid}/trimestre/{trimesterid}", response_model=list[NoteReponse1])
async def read_notes_by_student_and_trimester(
    eleveid: int ,
    trimesterid: int ,
    db: Database = Depends(MongoSingleton.get_db)
):
    return await get_notes_by_student_and_trimester(eleveid, trimesterid, db)


@router.get("/professeur/{professeur_id}/classe/{classe_id}", response_model=list[NoteReponse2])
async def read_notes_by_teacher_and_class(
    professeur_id: int = Path(..., title="The ID of the teacher"),
    classe_id: int = Path(..., title="The ID of the class"),
    db: Database = Depends(MongoSingleton.get_db)
):
    return await get_notes_by_teacher_and_class(classe_id, professeur_id, db)