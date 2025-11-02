from dotenv import load_dotenv
import os
import pandas as pd
from pymongo import MongoClient

# Charger les variables d'environnement
load_dotenv()

# Récupération des variables MongoDB
MDB_CONNECTION = os.getenv("MDB_CONNECTION")
MDB_BASE = os.getenv("MDB_BASE")
MDB_COLLECTION = os.getenv("MDB_COLLECTION")

# Connexion à la base MongoDB
client = MongoClient(MDB_CONNECTION)
db = client[MDB_BASE]
collection = db[MDB_COLLECTION]

# Chargement du CSV
df = pd.read_csv("anime_kaggle.csv")

# Conversion en dictionnaires
data = df.to_dict(orient="records")

# Insertion dans MongoDB
collection.insert_many(data)

print(f"{len(data)} documents insérés dans MongoDB")
