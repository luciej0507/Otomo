import requests
import json


# URL de l'API Jikan pour les genres d'anime
url = "https://api.jikan.moe/v4/genres/anime"
headers = {"User-Agent": "AnimeCollector/1.0 (contact: lucie.jouan@isen-ouest.yncrea.fr)"}

# Requête GET
response = requests.get(url)

# Vérification du statut
if response.status_code == 200:
    data = response.json()
    print("Genres récupérés avec succès !")

# Sauvegarde dans un fichier
with open("genres_anime.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Le JSON a été enregistré dans 'genres_anime.json'.")