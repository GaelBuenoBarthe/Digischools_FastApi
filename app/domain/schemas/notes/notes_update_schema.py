from pydantic import BaseModel


class NoteUpdateSchema(BaseModel):
    idnotes: int
    note: float

    class Config:
        from_attributes = True