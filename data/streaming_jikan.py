import pandas as pd
import requests
import json
import time
import random


# Chargement du fichier csv
df = pd.read_csv("anime_jikan_list.csv")
# Extrait la colonne 'anime_id' sous forme de liste
anime_ids = df['anime_id'].tolist()


# Interrogation de l'API Jikan
def get_streaming_links(anime_id, max_retries = 5):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/streaming"
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

# Récupération des plateformes de streaming pour les 300 animés
results = {}

for anime_id in anime_ids:
    data = get_streaming_links(anime_id)    # Appelle la fonction pour chaque ID
    if data is not None:                    # On vérifie que la réponse de l'API n'est pas vide
        results[str(anime_id)] = data.get("data", [])   # Stocke les plateformes de streaming
    else:
        results[str(anime_id)] = "Erreur ou données indisponibles"

    time.sleep(0.5)  # Pause entre chaque requête pour éviter de surcharger l'API

# Sauvegarde dans un fichier JSON
with open("streaming_links_all.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Liens de streaming enregistrés dans 'streaming_links_all.json'.")