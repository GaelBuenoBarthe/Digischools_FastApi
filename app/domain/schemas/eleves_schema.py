# Schéma pour l'entité Eleve (sans Pydantic)
EleveSchema = {
    "id": int,
    "nom": str,
    "prenom": str,
    "idclasse": int,  # ID de la classe de l'élève
    "date_naissance": str,
    "adresse": str,
    "sexe": str
}