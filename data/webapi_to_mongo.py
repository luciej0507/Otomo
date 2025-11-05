from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pandas as pd
import requests
import json
import time
import random
from tqdm import tqdm  # pour le suivi visuel

# Charger les variables d'environnement
load_dotenv()

# Récupération des variables de conenxion à MongoDB
MDB_CONNECTION = os.getenv("MDB_CONNECTION")
MDB_BASE = os.getenv("MDB_BASE")
MDB_COLLECTION_BIS = os.getenv("MDB_COLLECTION_BIS")

# Connexion à la base MongoDB
client = MongoClient(MDB_CONNECTION)
db = client[MDB_BASE]
collection = db[MDB_COLLECTION_BIS]


# Chargement du fichier csv
df = pd.read_csv("anime_jikan_list.csv")
anime_ids = df['anime_id'].tolist()         # Extrait la colonne 'anime_id' sous forme de liste



# Interrogation de l'API Jikan
def get_characters_and_va(anime_id, max_retries = 5):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/characters"
    headers = {"User-Agent": "AnimeCollector/1.0 (contact: lucie.jouan@isen-ouest.yncrea.fr)"}
    
    for attempt in range(max_retries):      # On tente plusieurs fois en cas d'erreur
        try:
            response = requests.get(url, headers=headers)
            
            # Si trop de requêtes envoyées (erreur 429), on attend avant de réessayer
            if response.status_code == 429:
                # Attente exponentielle + aléatoire
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Trop de requêtes (429). Pause de {wait_time:.1f}s avant retry...")
                time.sleep(wait_time)
                continue  # On recommence la boucle
            
            response.raise_for_status()     # Lève une erreur si le statut n'est pas OK
            return response.json()          # Retourne les données JSON si tout va bien
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur pour l'anime {anime_id} : {e}")
            time.sleep((2 ** attempt) + random.uniform(0, 1))   # Attente avant de retenter
    
    # Si toutes les tentatives échouent
    print(f"Abandon après {max_retries} tentatives pour {anime_id}")
    return None

# Récupération des personnages + doubleurs pour les 300 animés
characters_data = []

for i, anime_id in enumerate(tqdm(anime_ids)):  # Boucle avec barre de progression
    data = get_characters_and_va(anime_id)      # Appelle la fonction pour chaque id
    if data:
        characters_data.append({
            "anime_id": anime_id,
            "characters": data.get("data", [])  # Stocke les personnages (ou liste vide si absent)
        })

    # Pause aléatoire entre 0.4 et 0.7 secondes pour éviter de surcharger l'API
    time.sleep(random.uniform(0.4, 0.7))

    # Pause plus longue toutes les 60 requêtes pour respecter la limite de l'API
    if (i + 1) % 60 == 0:
        print("Pause de 90 secondes pour respecter la limite approximative de 60 req/min...")
        time.sleep(90)


# Insertion des résultats dans MongoDB
if characters_data:
    collection.insert_many(characters_data)      # Insère tous les documents dans la collection MongoDB
    print(f"{len(characters_data)} documents insérés dans la collection.")

