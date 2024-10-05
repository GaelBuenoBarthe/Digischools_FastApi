# Digischools FastAPI

Ce projet est une application de gestion d'école construite avec FastAPI, MongoDB et MySQL.

## Installation

Suivez ces étapes pour configurer et exécuter le projet :

### Prérequis

- Python 3.8+
- MongoDB
- MySQL

### Cloner le dépôt

```bash
git clone https://github.com/GaelBuenoBarthe/Digischools_FastApi.git
cd Digischools_FastApi
```
### Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  
Sur Windows utilisez `venv\Scripts\activate
```
### Installer les dépendances

```bash
pip install -r requirements.txt
``` 

### Configurer la base de données

MySQL : Utilisez phpMyAdmin pour importer le fichier SQL situé dans le dossier data pour créer la base de données MySQL.
MongoDB : Assurez-vous que MongoDB est en cours d'exécution et exécutez le script de migration pour créer la base de données MongoDB.

### Executer la migration 
Pour MongoDB, exécutez le script de migration situé dans le package util :
```bash
 python -m util.migrate
```
### Démarrer l'application
Pour démarrer l'application, exécutez la commande suivante :
```bash
uvicorn app.main:app --reload
```
### Utilisation
Une fois l'application en cours d'exécution, vous pouvez accéder à la documentation de l'API et tester les points de terminaison en utilisant Swagger UI.

Accéder à Swagger UI
Ouvrez votre navigateur et accédez à : http://127.0.0.1:8000
puis cliquer sur le lien API Documentation du bandeau supérieur

### Points de terminaison de l'API :

Voici quelques-uns des principaux points de terminaison que vous pouvez utiliser :  
Créer une note : POST /notes
Obtenir les notes par élève : GET /notes/student/{eleve_id}
Obtenir les notes par professeur : GET /notes/teacher/{professeur_id}
Obtenir les notes par classe : GET /notes/class/{classe_id}
Obtenir les notes par trimestre : GET /notes/trimester/{trimester_id}
Obtenir les notes par élève et trimestre : GET /notes/student/{eleve_id}/trimester/{trimester_id}
Obtenir les notes par professeur et classe : GET /notes/teacher/{professeur_id}/class/{classe_id}

### Powerpoint

Le powerpoint de présentation du projet est disponible dans le dossier ressources.

### License

Bernardo Estacio Abreu
Fabrice Bellin
Gael Bueno Barthe


