import requests
from bs4 import BeautifulSoup
import json

# URL de la page à scraper
url = "https://www.boredpanda.com/anime-quotes/"

# Envoi de la requête GET avec un User-Agent pour éviter les blocages
resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

# Récupération du contenu HTML brut de la réponse
html = resp.text

# Vérification du statut de la requête
if resp.status_code == 200: 
    print("Succès ! Contenu de la page récupéré.") 

    # Sauvegarde du HTML dans un fichier local (pour archivage ou debug)
    with open("../data/anime_quotes.html", "w", encoding="utf-8") as f: 
        f.write(resp.text) 
else: 
    print(f"Erreur : statut {resp.status_code}")


# Création d'un objet BeautifulSoup pour pouvoir naviguer dans le HTML 
soup = BeautifulSoup(html, 'html.parser')

# Récupération de tous les éléments <span> contenant les citations
quotes = soup.find_all("span", class_="bordered-description with-image")

# Création d'une liste contenant le texte brut de chaque citation, sans les balises
quotes_list = [quote.get_text(strip=True) for quote in quotes]

# Structuration des données dans un dictionnaire avec métadonnées
output = {
    "source": "https://www.boredpanda.com/anime-quotes/",   # URL d’origine
    "retrieved_at": "2025-10-24",                           # date de récupération
    "quotes": quotes_list                                   # liste brute des citations
}

# Sauvegarde du résultat dans un fichier JSON lisible
with open("../data/anime_quotes.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)