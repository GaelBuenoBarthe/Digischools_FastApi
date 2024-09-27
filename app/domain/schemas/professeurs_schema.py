# Schéma pour l'entité Professeur (sans Pydantic)
ProfesseurSchema = {
    "id": int,
    "nom": str,
    "prenom": str,
    "date_naissance": str,  # Ou datetime si vous préférez gérer les dates en Python
    "adresse": str,
    "sexe": str
}