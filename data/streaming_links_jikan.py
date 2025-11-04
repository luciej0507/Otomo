import pandas as pd
import requests
import json
import time
import random
from tqdm import tqdm  # pour le suivi visuel

# Chargement du fichier csv
df = pd.read_csv("anime_jikan_list.csv")
anime_ids = df['anime_id'].tolist()


# Interrogation de l'API Jikan
def get_streaming_links(anime_id, max_retries = 5):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/streaming"
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

# Récupération des données pour tous les animés
results = {}

for anime_id in anime_ids:
    data = get_streaming_links(anime_id)
    if data is not None:
        results[str(anime_id)] = data.get("data", [])
    else:
        results[str(anime_id)] = "Erreur ou données indisponibles"

    time.sleep(0.5)  # Pause pour éviter le spam

# Sauvegarde dans un fichier JSON
with open("streaming_links_all.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Liens de streaming enregistrés dans 'streaming_links_all.json'.")