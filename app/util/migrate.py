import mysql.connector
from app.util.mongo_singleton import get_db, MongoSingleton

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
mongo_db = get_db()

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

    # Si la table a des sous-collections , crée les sous-collections
    if mysql_table in table_structure:
        for record in records:
            transformed_record = transform_record(record, table_structure[mysql_table])
            # Use the primary key as the filter for upsert
            primary_key = list(record.keys())[0]
            # Verifiersi la donnée existe déjà dans la collection pour éviter les doublons
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
            # Verifier si la donnée existe déjà dans MongoDB pour éviter les doublons
            existing_record = mongo_db[mongo_collection].find_one({primary_key: record[primary_key]})
            if not existing_record:
                mongo_db[mongo_collection].update_one(
                    {primary_key: record[primary_key]},
                    {"$set": record},
                    upsert=True
                )

# Fermeture des connexions
mysql_cursor.close()
mysql_conn.close()
MongoSingleton().close()

# Message de succès
print("Base de données créée et remplie avec succès avec sous-collections, sans doublons.")