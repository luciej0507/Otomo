# Projet Otomo

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" />
   <img src="https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/SQL-4479A1?logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

---
## Sommaire

1. [Présentation](#présentation)
2. [Architecture du projet](#architecture-du-projet)
3. [Technologies utilisées](#technologies-utilisées)
4. [Installation et exécution](#installation-et-exécution)
5. [Création et chargement des bases de données](#création-et-chargement-des-bases-de-données)
6. [API REST](#api-rest)
7. [Licence](#licence)
8. [Auteur](#auteur)

---

## 1. Présentation

Le projet OTOMO est né d'une passion pour l'animation japonaise et d’un constat : les informations sur les animés sont nombreuses mais très souvent éparpillées entre de nombreuses plateformes, sites en tout genre et notes personnelles.

N'ayant pas trouvé d’outils qui répondait à ce besoin de centraliser toutes ces informations en seul et même endroit, c’est alors que l’idée du projet OTOMO est apparue. Ce terme, signifiant "compagnon" en japonais, reflète l'ambition du projet : créer un compagnon numérique pour les passionnés d'animés, rassemblant différentes informations sur une plateforme unique.

Les étapes présentées ci-dessous retrace la première phase du projet dont l’objectif est d’automatiser la collecte, le stockage et la mise à disposition des données nécessaire pour la réalisation de l’outil.

Le projet, s’inscrivant dans un cadre pédagogique, a été réalisé en utilisant uniquement des outils open source et des ressources disponibles gratuitement.

Le pipeline global repose sur 3 étapes clés :

1. **Extraction, transformation et agrégation** de 5 sources de données :  
   - API Jikan (données MyAnimeList)  
   - Dataset Big Data (Kaggle)  
   - Fichier texte personnel  
   - Base SQLite (utilisateurs fictifs)  
   - Webscraping (citations d'animés)

2. **Chargement** des données dans une base MySQL.

3. **Mise à disposition** des données via une API REST FastAPI, sécurisée par JWT.

---

## 2. Architecture du projet

```bash
otomo/
│── data/                               # 5 sources de données brutes
│── database/                           # Base Mysql
│       ├── otomo_db.py                 # Script de création de la Base Mysql
│── etl_scripts/                        # Extraction, transformation et chargement
│       ├── etl_api_jikan.py            # ETL de la source : WebAPI
│       ├── etl_fichier_perso.py        # ETL de la source : fichier
│       ├── etl_kaggle_bigdata.py       # ETL de la source : Big Data
│       ├── etl_utilisateur.py          # ETL de la source : base SQLite
│       ├── etl_webscraping.py          # ETL de la source : webscraping
│       ├── run_all_etl.py              # Script principal qui lance tous les ETL dans l'ordre
├── notebook/                           # Analyses exploratoires
│       ├── explore_kaggle_mongo_ipynb  # Exploration du dataset kaggle
├── serveur_api_rest/                   # API REST
│       ├── crud/                       # Fonctions CRUD (SQL)
│       ├── routers/                    # Routes API
│       ├── schemas/                    # Modèles Pydantic
│       ├── auth.py                     # Authentification JWT
│       ├── database.py                 # Connexion à MySQL
│       └── main.py                     # Point d'entrée FastAPI
├── .env.exemple                        # Modèle pour créer variables d'environnement
├── docker-compose.yml                  # Déploiement Docker (MySQL, Adminer, MongoDB)
└── requirement.txt                     # Dépendances Python
```

---

## 3. Technologies utilisées

- **Langage :** Python 3.11  
- **Framework API :** FastAPI  
- **Bases de données :**
  - MySQL (base de données relationnelle finale)
  - MongoDB (stockage des données issues du Big Data et de l’API)
  - SQLite (gestion d’utilisateurs fictifs)
- **Librairies principales :**
  - `pandas`, `requests`, `beautifulsoup4`
  - `mysql.connector`, `pymongo`, `sqlite3`
  - `bcrypt`, `python-jose`, `pydantic`
- **Conteneurs Docker :** Mysql, Adminer et MongoDB
    
---

## 4. Installation et exécution

```bash
# Cloner le projet
git clone https://github.com/luciej0507/Otomo.git
cd otomo

# Créer un environnement virtuel
python -m venv .venv

# Activer l'environnement
# sous Linux/Mac
source .venv/bin/activate
# sous Windows
.venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Définir ces variables d'environnement
.env.exemple

# Lancer les conteneurs Docker (MySQL, Adminer et MongoDB)
docker compose up -d
```

---

## 5. Création et chargement des bases de données

- **Base SQLite**
```bash
# Création de la base et ajout des utilisateur depuis le terminal
cd data
python3 create_users_sqlite.py
```

- **Base MongoDB :** créée lorsque les données sont chargées dans la base et la collection définies dans le .env

- **Base SQL :**
```bash
# Création de la base de données SQL
cd database
python3 otomo_db.py
```

- **Chargement des données dans la base SQL :**
```bash
# Lancer les scripts ETL
cd etl_scripts
python3 run_all_etl.py
```

---

## 6. API REST
```bash
# Lancer le serveur FastAPI
cd otomo
uvicorn serveur_api_rest.main:app --reload --host 0.0.0.0 --port 8081
```
L’API est disponible à l'adresse : [http://localhost:8081](http://localhost:8081)

Documentation OpenAPI (Swagger) : [http://localhost:8081/docs](http://localhost:8081/docs)

### Authentification :
- Conenxion via la route /login
- Un token JWT est fourni et doit être entré dans l'en-tête Authorize

---

## ![License](https://img.shields.io/badge/License-MIT-yellow) Licence
- Licence : [MIT](LICENSE)

### ![Author](https://img.shields.io/badge/Team-Author-blue) Auteur
- [Lucie Jouan](https://github.com/luciej0507) 
Projet réalisé dans le cadre du Bloc de Compétences E1 de la formation "Développeur en intelligence artificielle" (Ecole IA by Simplon / ISEN)
