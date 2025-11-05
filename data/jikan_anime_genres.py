import requests
import json


# URL de l'API Jikan pour la liste des genres d'animés
url = "https://api.jikan.moe/v4/genres/anime"
# En-tête HTTP personnalisé
headers = {"User-Agent": "AnimeCollector/1.0 (contact: lucie.jouan@isen-ouest.yncrea.fr)"}

# Requête GET à l'API
response = requests.get(url)

# Si la requête est réussie (code 200), on récupère les données JSON
if response.status_code == 200:
    data = response.json()
    print("Genres récupérés avec succès !")

# Sauvegarde des données dans un fichier local (pour contrôle)
with open("genres_anime.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Les données ont été enregistrées dans 'genres_anime.json'.")