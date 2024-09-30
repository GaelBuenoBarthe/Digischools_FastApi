from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.domain.schemas.matieres_schema import MatiereSchema
from app.api.controller.matieres_controller import get_all_matieres, get_matiere_by_id

router = APIRouter()

@router.get("/", response_model=List[MatiereSchema])
async def read_matieres():
    return await get_all_matieres()

@router.get("/{idmatiere}", response_model=MatiereSchema)
async def read_matiere(idmatiere: int):
    return await get_matiere_by_id(idmatiere)