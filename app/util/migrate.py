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
mongo_db = MongoSingleton

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
    "t_eleve": "élèves",
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
            existing_record = mongo_db.get_db()[mongo_collection].find_one({primary_key: record[primary_key]})
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
            existing_record = mongo_db.get_db()[mongo_collection].find_one({primary_key: record[primary_key]})
            if not existing_record:
                mongo_db[mongo_collection].update_one(
                    {primary_key: record[primary_key]},
                    {"$set": record},
                    upsert=True
                )

# Création des vues dans MongoDB (uniquement après la migration des données)

def create_mongo_views():
    # View for Student and Trimester Aggregation
    mongo_db.get_db().command({
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
                    "_id.eleve_id": 1,  # Sort by student ID (ascending)
                    "_id.trimestre_id": 1  # Sort by trimester ID (ascending)
                }
            },
            {
                "$project": {
                    "_id": 0,  # Exclude the internal MongoDB _id field from the output
                    "eleve_id": "$_id.eleve_id",  # Include the student ID
                    "eleve_nom": 1,  # Include the student name
                    "eleve_prenom": 1,  # Include the student first name
                    "classe": 1,  # Include the class
                    "trimestre_id": "$_id.trimestre_id",  # Include the trimester ID
                    "trimestre_nom": 1,  # Include the trimester name
                    "trimestre_start": 1,  # Include the trimester start date
                    "notes": 1,  # Include the list of notes
                    "average_note": 1  # Include the average note
                }
            }
        ]
    })

    # View for Teacher and Class Aggregation
    mongo_db.get_db().command({
        'create': 'view_teacher_class',
        'viewOn': 'notes',
        'pipeline': [
            {
                "$lookup": {
                    "from": "classes",  # Join with the classes collection
                    "localField": "idclasse",  # Local field from notes
                    "foreignField": "id",  # Foreign field from classes
                    "as": "class_details"  # Output array field for class details
                }
            },
            {
                "$lookup": {
                    "from": "élèves",  # Join with the students collection
                    "localField": "ideleve",  # Local field from notes
                    "foreignField": "id",  # Foreign field from students
                    "as": "student_details"  # Output array field for student details
                }
            },
            {
                "$lookup": {
                    "from": "professeurs",  # Join with the teachers collection
                    "localField": "idprof",  # Local field from notes
                    "foreignField": "id",  # Foreign field from teachers
                    "as": "prof_details"  # Output array field for teacher details
                }
            },
            {
                "$unwind": "$idclasse"  # Unwind the class details
            },
            {
                "$unwind": "$ideleve"  # Unwind the student details
            },
            {
                "$unwind": "$idprof"  # Unwind the teacher details
            },
            {
                "$group": {
                    "_id": {
                        "idnotes": "$idnotes",  # Group by note ID
                        "ideleve": "$ideleve",  # Group by student ID
                        "idclasse": "$idclasse",  # Group by class ID
                        "idmatiere": "$idmatiere",  # Group by subject ID
                        "idprof": "$idprof"  # Group by teacher ID
                    },
                    "note": {"$first": "$note"},  # Get the note
                    "date_saisie": {"$first": "$date_saisie"},  # Get the entry date
                    "avis": {"$first": "$avis"},  # Get comments
                    "avancement": {"$first": "$avancement"},  # Get progress
                    "class": {"$first": "$idclasse"},  # Get class details
                    "student": {"$first": "$ideleve"},  # Get student details
                    "prof": {"$first": "$idprof"}  # Get teacher details
                }
            },
            {
                "$project": {
                    "_id": 0,  # Exclude the internal MongoDB _id field from the output
                    "idnotes": "$_id.idnotes",  # Include the note ID
                    "note": 1,  # Include the note
                    "date_saisie": 1,  # Include the entry date
                    "avis": 1,  # Include comments
                    "avancement": 1,  # Include progress
                    "class": 1,  # Include class details
                    "student": 1,  # Include student details
                    "prof": 1  # Include teacher details
                }
            }
        ]
    })



# Only create views after data migration is complete
create_mongo_views()

# Fermeture des connexions
mysql_cursor.close()
mysql_conn.close()
mongo_db.close(mongo_db)

# Message de succès
print("Base de données créée et remplie avec succès avec sous-collections, sans doublons. Vues créées avec succès.")
