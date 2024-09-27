import mysql.connector
import pymongo

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
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client.digischools


# Function to get a record by primary key from MySQL
def get_record_by_id(table, id_field, id_value):
    mysql_cursor.execute(f"SELECT * FROM {table} WHERE {id_field} = %s", (id_value,))
    return mysql_cursor.fetchone()


# Function to transform foreign key IDs into subcollections
def transform_record(record, table_structure):
    for field, ref_table in table_structure.items():
        if field in record:
            ref_record = get_record_by_id(ref_table['table'], ref_table['id_field'], record[field])
            if ref_record:
                record[field] = ref_record  # Embed the full referenced record instead of the ID
    return record


# Table structure to define relationships for all tables
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
    "t_prof": {},  # No foreign keys in t_prof
    "t_matiere": {},  # No foreign keys in t_matiere
    "t_trimestre": {}  # No foreign keys in t_trimestre
}

# Export and transform data from MySQL to MongoDB
tables = {
    "t_prof": "professeurs",
    "t_eleve": "élèves",
    "t_notes": "notes",
    "t_trimestre": "trimestres",
    "t_matiere": "matieres",
    "t_classe": "classes",
}

# Insertion of data into MongoDB with subcollections
for mysql_table, mongo_collection in tables.items():
    mysql_cursor.execute(f"SELECT * FROM {mysql_table}")
    records = mysql_cursor.fetchall()

    # If this table has relationships, apply the transformation for subcollections
    if mysql_table in table_structure:
        for record in records:
            transformed_record = transform_record(record, table_structure[mysql_table])
            # Use the primary key as the filter for upsert
            primary_key = list(record.keys())[0]
            # Check if the record already exists in MongoDB to avoid duplicates
            existing_record = mongo_db[mongo_collection].find_one({primary_key: record[primary_key]})
            if not existing_record:
                mongo_db[mongo_collection].update_one(
                    {primary_key: record[primary_key]},
                    {"$set": transformed_record},
                    upsert=True
                )
    else:
        # No relationships, insert directly
        for record in records:
            primary_key = list(record.keys())[0]
            # Check if the record already exists in MongoDB to avoid duplicates
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
mongo_client.close()

# Message de succès
print("Base de données créée et remplie avec succès avec sous-collections, sans doublons.")
