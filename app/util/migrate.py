import mysql.connector
from app.util.mongo_singleton import MongoSingleton

# Connexion à MySQL
mysql_conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="digischools",
    password="digischools",
    database="digischools"
)
mysql_cursor = mysql_conn.cursor(dictionary=True)

# Connexion à MongoDB
mongo_db = MongoSingleton.get_db()

# Fonction pour obtenir un enregistrement par ID
def get_record_by_id(table, id_field, id_value):
    mysql_cursor.execute(f"SELECT * FROM {table} WHERE {id_field} = %s", (id_value,))
    return mysql_cursor.fetchone()

# Fonction pour transformer les enregistrements en remplaçant les ID par les enregistrements complets
def transform_record(record, table_structure):
    for field, ref_table in table_structure.items():
        if field in record:
            ref_record = get_record_by_id(ref_table['table'], ref_table['id_field'], record[field])
            if ref_record:
                record[field] = ref_record  # Embed the full referenced record instead of the ID
    return record

# Structure des tables avec les sous-collections
table_structure = {
    "t_notes": {
        "idclasse": {"table": "t_classe", "id_field": "id"},
        "ideleve": {"table": "t_eleve", "id_field": "id"},
        "idmatiere": {"table": "t_matiere", "id_field": "idmatiere"},
        "idprof": {"table": "t_prof", "id_field": "id"},
        "idtrimestre": {"table": "t_trimestre", "id_field": "idtrimestre"}
    },
    "t_classe": {
        "prof": {"table": "t_prof", "id_field": "id"}
    },
    "t_eleve": {
        "classe": {"table": "t_classe", "id_field": "id"}
    },
    "t_prof": {},
    "t_matiere": {},
    "t_trimestre": {}
}

# Exporte les données de MySQL vers MongoDB
tables = {
    "t_prof": "professeurs",
    "t_eleve": "eleves",
    "t_notes": "notes",
    "t_trimestre": "trimestres",
    "t_matiere": "matieres",
    "t_classe": "classes",
}

# Insertion des données dans MongoDB avec des sous-collections
for mysql_table, mongo_collection in tables.items():
    mysql_cursor.execute(f"SELECT * FROM {mysql_table}")
    records = mysql_cursor.fetchall()

    # Si la table a des sous-collections, crée les sous-collections
    if mysql_table in table_structure:
        for record in records:
            transformed_record = transform_record(record, table_structure[mysql_table])
            # Use the primary key as the filter for upsert
            primary_key = list(record.keys())[0]
            # Vérifier si la donnée existe déjà dans la collection pour éviter les doublons
            existing_record = mongo_db[mongo_collection].find_one({primary_key: record[primary_key]})
            if not existing_record:
                mongo_db[mongo_collection].update_one(
                    {primary_key: record[primary_key]},
                    {"$set": transformed_record},
                    upsert=True
                )
    else:
        # Pas de sous-collections, insertion directe
        for record in records:
            primary_key = list(record.keys())[0]
            # Vérifier si la donnée existe déjà dans MongoDB pour éviter les doublons
            existing_record = mongo_db[mongo_collection].find_one({primary_key: record[primary_key]})
            if not existing_record:
                mongo_db[mongo_collection].update_one(
                    {primary_key: record[primary_key]},
                    {"$set": record},
                    upsert=True
                )

# Création des vues dans MongoDB (uniquement après la migration des données)
def create_mongo_views():
    # View for Student and Trimester Aggregation
    mongo_db.command({
        'create': 'view_stu_tri',
        'viewOn': 'notes',
        'pipeline': [
            {
                "$unwind": "$ideleve"  # Flatten the 'ideleve' field (student info)
            },
            {
                "$unwind": "$idtrimestre"  # Flatten the 'idtrimestre' field (trimester info)
            },
            {
                "$group": {
                    "_id": {
                        "eleve_id": "$ideleve.id",  # Group by student ID
                        "trimestre_id": "$idtrimestre.idtrimestre"  # Group by trimester ID
                    },
                    "eleve_nom": {"$first": "$ideleve.nom"},  # Get student name
                    "eleve_prenom": {"$first": "$ideleve.prenom"},  # Get student first name
                    "classe": {"$first": "$ideleve.classe"},  # Get the student's class
                    "trimestre_nom": {"$first": "$idtrimestre.nom"},  # Get trimester name
                    "trimestre_start": {"$first": "$idtrimestre.date"},  # Get the trimester start date
                    "notes": {"$push": "$note"},  # Collect all the notes related to the student
                    "average_note": {"$avg": "$note"}  # Calculate the average note for the student in that trimester
                }
            },
            {
                "$sort": {
                    "_id.eleve_id": 1,
                    "_id.trimestre_id": 1
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "eleve_id": "$_id.eleve_id",
                    "eleve_nom": 1,
                    "eleve_prenom": 1,
                    "classe": 1,
                    "trimestre_id": "$_id.trimestre_id",
                    "trimestre_nom": 1,
                    "trimestre_start": 1,
                    "notes": 1,
                    "average_note": 1
                }
            }
        ]
    })

    # View for Teacher and Class Aggregation
    mongo_db.command({
        'create': 'view_teacher_lecture',  # Name of the view
        'viewOn': 'notes',  # Base collection to create the view from
        'pipeline': [
            {
                "$addFields": {
                    "classe_id": "$idclasse.id",
                    "classe_nom": "$idclasse.nom",
                    "classe_prof": "$idclasse.prof",

                    "eleve_id": "$ideleve.id",
                    "eleve_nom": "$ideleve.nom",
                    "eleve_prenom": "$ideleve.prenom",
                    "eleve_classe": "$ideleve.classe",
                    "eleve_date_naissance": "$ideleve.date_naissance",
                    "eleve_adresse": "$ideleve.adresse",
                    "eleve_sexe": "$ideleve.sexe",

                    "matiere_id": "$idmatiere.idmatiere",
                    "matiere_nom": "$idmatiere.nom",

                    "prof_id": "$idprof.id",
                    "prof_nom": "$idprof.nom",
                    "prof_prenom": "$idprof.prenom",
                    "prof_date_naissance": "$idprof.date_naissance",
                    "prof_adresse": "$idprof.adresse",
                    "prof_sexe": "$idprof.sexe",

                    "trimestre_id": "$idtrimestre.idtrimestre",
                    "trimestre_nom": "$idtrimestre.nom",
                    "trimestre_start": "$idtrimestre.date",

                    "note": "$note"
                }
            },
            {
                "$group": {
                    "_id": {
                        "classe_id": "$classe_id",  # Group by class ID
                        "prof_id": "$prof_id"  # Group by professor ID
                    },
                    "classe_nom": {"$first": "$classe_nom"},
                    "classe_prof": {"$first": "$classe_prof"},
                    "prof_nom": {"$first": "$prof_nom"},
                    "prof_prenom": {"$first": "$prof_prenom"},
                    "notes": {
                        "$push": {
                            "eleve_id": "$eleve_id",
                            "eleve_nom": "$eleve_nom",
                            "eleve_prenom": "$eleve_prenom",
                            "matiere_nom": "$matiere_nom",
                            "trimestre_nom": "$trimestre_nom",
                            "trimestre_start": "$trimestre_start",
                            "note": "$note"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,  # Exclude the MongoDB internal _id field
                    "classe_id": "$_id.classe_id",
                    "prof_id": "$_id.prof_id",
                    "classe_nom": 1,
                    "classe_prof": 1,
                    "prof_nom": 1,
                    "prof_prenom": 1,
                    "notes": 1
                }
            }
        ]
    })

# Only create views after data migration is complete
create_mongo_views()

# Fermeture des connexions
mysql_cursor.close()
mysql_conn.close()
MongoSingleton().close()

# Message de succès
print("Base de données créée et remplie avec succès avec sous-collections, sans doublons.")
