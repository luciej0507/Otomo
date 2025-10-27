from pymongo import MongoClient
import pandas as pd
import requests
import json
import time
import random
from tqdm import tqdm  # pour le suivi visuel

# Connexion à la base MongoDB
client = MongoClient("mongodb://hobby:hobby@localhost:27017/admin")
db = client["anime"]
collection = db["characters"]

# Chargement du fichier csv
df = pd.read_csv("anime_jikan_list.csv")
anime_ids = df['anime_id'].tolist()



# Interrogation de l'API Jikan
def get_characters_and_va(anime_id, max_retries = 5):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/characters"
    headers = {"User-Agent": "AnimeCollector/1.0 (contact: lucie.jouan@isen-ouest.yncrea.fr)"}
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            
            # Si le serveur revoit "429 - Too Many Request"
            if response.status_code == 429:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Trop de requêtes (429). Pause de {wait_time:.1f}s avant retry...")
                time.sleep(wait_time)
                continue  # retente
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur pour l'anime {anime_id} : {e}")
            time.sleep((2 ** attempt) + random.uniform(0, 1))
    
    print(f"Abandon après {max_retries} tentatives pour {anime_id}")
    return None
        
characters_data = []

for i, anime_id in enumerate(tqdm(anime_ids)):
    data = get_characters_and_va(anime_id)
    if data:
        characters_data.append({
            "anime_id": anime_id,
            "characters": data.get("data", [])
        })

    # Délai aléatoire entre 0.4 et 0.7 sec pour respecter le rate limiting
    time.sleep(random.uniform(0.4, 0.7))

    if (i + 1) % 60 == 0:
        print("Pause de 90 secondes pour respecter la limite approximative de 60 req/min...")
        time.sleep(90)

if characters_data:
    collection.insert_many(characters_data)
    print(f"{len(characters_data)} documents insérés dans la collection.")

