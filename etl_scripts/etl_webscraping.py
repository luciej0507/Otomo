from dotenv import load_dotenv
import os
import json
import re
import unicodedata
import mysql.connector


# Charger les variables d'environnement
load_dotenv()

# Connexion MySQL
DB_HOST = os.getenv("DB_HOST")
DB_ROOT = os.getenv("DB_ROOT")
DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# connexion à la base SQL
admin_cnx = mysql.connector.connect(
    host=DB_HOST,
    user=DB_ROOT,      
    password=DB_ROOT_PASSWORD,
    database=DB_NAME
)

admin_cursor = admin_cnx.cursor(dictionary=True, buffered=True)


### --- EXTRACTION ---
# Chargement du fichier JSON brut avec toutes les citations
with open("../data/anime_quotes.json", "r", encoding="utf-8") as f:
    data = json.load(f)


### --- TRANFORMATION ---
# Préparation de la liste des citations transformées
transformed_quotes = []

# Pattern pour extraire la citation, le personnage et l'animé
pattern = r'[“"](.*?)[”"]\s*[—-]\s*(.*?),\s*(.*)'

for raw_quote in data["quotes"]:
    match = re.match(pattern, raw_quote)
    if match:
        quote_text = match.group(1).strip()
        character_name = match.group(2).strip()
        anime_title = match.group(3).strip()

        transformed_quotes.append({
            "quote_text": quote_text,
            "character_name": character_name,
            "anime_title": anime_title
        })
    else:
        print(f"Format inattendu : {raw_quote}")

# Sauvegarde du JSON structuré
with open("anime_quotes_clean.json", "w", encoding="utf-8") as f:
    json.dump(transformed_quotes, f, ensure_ascii=False, indent=2)

def normalize_title(title):
    import unicodedata
    title = title.lower()
    title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("utf-8")
    title = title.replace(":", "").replace("-", " ").replace("’", "'").strip()
    return title


### --- CHARGEMENT ---
# Table CITATION
# Trouver l’id de l’anime correspondant à son title
def get_anime_id(anime_title):
    admin_cursor.execute("""
        SELECT id FROM anime
        WHERE LOWER(titre_anglais) LIKE LOWER(%s)
           OR LOWER(titre_original) LIKE LOWER(%s)
        ORDER BY LENGTH(titre_anglais) ASC
        LIMIT 1
    """, (f"%{anime_title}%", f"%{anime_title}%"))
    result = admin_cursor.fetchone()
    return result["id"] if result else None

# Trouver l’id du personnage lié à un anime précis
def get_character_id(character_name, anime_id):
    admin_cursor.execute("""
        SELECT p.id FROM personnage p
        JOIN anime_personnage ap ON p.id = ap.personnage_id
        WHERE (LOWER(p.nom_perso) LIKE LOWER(%s)
            OR LOWER(p.nom_perso) LIKE LOWER(%s))
          AND ap.anime_id = %s
    """, (f"%{character_name}%", f"%{' '.join(character_name.split()[::-1])}%", anime_id))
    result = admin_cursor.fetchone()
    return result["id"] if result else None

# Insérer une nouvelle citation dans la table citation
def insert_citation(quote_text, anime_id, character_id):
    admin_cursor.execute("""
        INSERT INTO citation (citation, anime, personnage)
        VALUES (%s, %s, %s)
    """, (quote_text, anime_id, character_id))
    admin_cnx.commit()


# Insertion dans la table 
for quote in transformed_quotes:
    anime_title = normalize_title(quote["anime_title"])

    anime_id = get_anime_id(anime_title)
    if not anime_id:
        continue

    character_id = get_character_id(quote["character_name"], anime_id)
        
    insert_citation(
        quote_text=quote["quote_text"],
        anime_id=anime_id,
        character_id=character_id  # peut être None si le personnage est absent
    )


# Commit et fermeture
admin_cnx.commit()
admin_cursor.close()
admin_cnx.close()