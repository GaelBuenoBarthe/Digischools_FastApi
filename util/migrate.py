import mysql.connector
import pymongo
from pymongo.errors import DuplicateKeyError

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

# Export des données de MySQL vers MongoDB
tables = {
    "t_prof": "professeurs",
    "t_eleve": "élèves",
    "t_notes": "notes",
    "t_trimestre": "trimestres",
    "t_matiere": "matieres",
    "t_classe": "classes",
}

# Insertion des données dans MongoDB
for mysql_table, mongo_collection in tables.items():
    mysql_cursor.execute(f"SELECT * FROM {mysql_table}")
    records = mysql_cursor.fetchall()
    for record in records:
        try:
            mongo_db[mongo_collection].insert_one(record)
        except DuplicateKeyError:
            continue

# Fermeture des connexions
mysql_cursor.close()
mysql_conn.close()
mongo_client.close()

# Message de succès
print("Base de données créée et remplie avec succès.")