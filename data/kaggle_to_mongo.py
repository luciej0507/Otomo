import pandas as pd
from pymongo import MongoClient
from config_mongo import MDB_CONNECTION, MDB_BASE, MDB_COLLECTION

# Connexion à MongoDB
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
