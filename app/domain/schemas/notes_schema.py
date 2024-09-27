# Schéma pour l'entité Note (sans Pydantic)
NoteSchema = {
    "idnotes": int,
    "ideleve": int,
    "idclasse": int,
    "idmatiere": int,
    "idprof": int,
    "idtrimestre": int,
    "note": int,
    "date_saisie": str,
    "avis": str,
    "avancement": float
}