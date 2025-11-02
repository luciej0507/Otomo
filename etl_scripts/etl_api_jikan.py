from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pandas as pd
import mysql.connector


# Charger les variables d'environnement
load_dotenv()

# Connexion MongoDB
MDB_CONNECTION = os.getenv("MDB_CONNECTION")
MDB_BASE = os.getenv("MDB_BASE")
MDB_COLLECTION_BIS = os.getenv("MDB_COLLECTION")

client = MongoClient(MDB_CONNECTION)
db = client[MDB_BASE]
collection = db[MDB_COLLECTION_BIS]


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

admin_cursor = admin_cnx.cursor()



### --- EXTRACTION ---
# extraction des personnages dont le rôle est "Main" et "Supporting"
# Liste pour stocker les résultats
results = []

# Parcours des documents
for doc in collection.find():
    anime_id = doc.get("anime_id", "Unknown ID")
    characters = doc.get("characters", [])

    # on ne garde que les roles "Main" et "Supporting"
    mains = [char for char in characters if char.get("role") == "Main"]
    supportings = [char for char in characters if char.get("role") == "Supporting"]
    # Tri des personnages secondaires par popularité décroissante
    supportings_sorted = sorted(
        supportings,
        key=lambda x: x.get("favorites", 0),
        reverse=True
    )
    # on garde les 5 premiers
    sampled_supportings = supportings_sorted[:5]

    selected_chars = mains + sampled_supportings

    for char in selected_chars:
        char_info = char.get("character", {})
        char_name = char_info.get("name")

        for va in char.get("voice_actors", []):
            if va.get("language") == "Japanese": # seuls les doubleurs japonais sont conservés
                va_info = va.get("person", {})
                va_name = va_info.get("name")
                va_url = va_info.get("url")

                results.append({
                    "anime_id": anime_id,
                    "character": char_name,
                    "role": char.get("role"),
                    "voice_actor": va_name,
                    "voice_actor_url": va_url
                })


# Conversion en DataFrame
df = pd.DataFrame(results)



### --- TRANSFORMATION ---
## Harmonisation des noms des personnages et des voice actors
def invert_name(name):
    if name and "," in name:
        last, first = name.split(",", 1)
        return f"{first.strip()} {last.strip()}"
    return name

df["character"] = df["character"].apply(invert_name)
df["voice_actor"] = df["voice_actor"].apply(invert_name)


## Récupération des voice actors uniques
voice_df = df[["voice_actor", "voice_actor_url"]].dropna().drop_duplicates()

## Récupération des personnages uniques
unique_perso = df[["character", "role"]].dropna().drop_duplicates()



### --- CHARGEMENT ---
## Table VOICE_ACTOR
for row in voice_df.itertuples(index=False):
    nom_va = row.voice_actor
    url_profil = row.voice_actor_url
    try:
        admin_cursor.execute(
            "INSERT INTO voice_actor (nom_va, url_profil) VALUES (%s, %s);",
            (nom_va, url_profil,)
        )
    except Exception as e:
        print(f"Erreur pour {nom_va}: {e}")



## Table PERSONNAGE unique
for row in unique_perso.itertuples(index=False):
    nom_perso = row.character
    role = row.role
    admin_cursor.execute(
        "INSERT INTO personnage (nom_perso, role) VALUES (%s, %s);",
        (nom_perso, role)
    )


## Tables de liaison anime_personnage et perso_voice_actor
# Charger les tables SQL
admin_cursor.execute("SELECT id AS anime_sql_id, anime_id FROM anime;")
anime_df = pd.DataFrame(admin_cursor.fetchall(), columns=["anime_sql_id", "anime_id"])

admin_cursor.execute("SELECT id AS voice_actor_id, nom_va FROM voice_actor;")
va_df = pd.DataFrame(admin_cursor.fetchall(), columns=["voice_actor_id", "voice_actor"])

admin_cursor.execute("SELECT id AS personnage_id, nom_perso FROM personnage;")
perso_df = pd.DataFrame(admin_cursor.fetchall(), columns=["personnage_id", "nom_perso"])

# Fusionner avec le df
df_merged = df.merge(anime_df, on="anime_id", how="left")
df_merged = df_merged.merge(va_df, on="voice_actor", how="left")
df_merged = df_merged.merge(perso_df, left_on="character", right_on="nom_perso", how="left")

# Remplissage de la table anime_personnage
for _, row in df_merged.iterrows():
    try:
        admin_cursor.execute("""
            INSERT IGNORE INTO anime_personnage (personnage_id, anime_id)
            VALUES (%s, %s);
        """, (row["personnage_id"], row["anime_sql_id"]))
    except Exception as e:
        print(f"Erreur anime_personnage pour {row['character']}: {e}")

# Remplissage de la table perso_voice_actor
for _, row in df_merged.iterrows():
    try:
        admin_cursor.execute("""
            INSERT IGNORE INTO perso_voice_actor (personnage_id, voice_actor_id)
            VALUES (%s, %s);
        """, (row["personnage_id"], row["voice_actor_id"]))
    except Exception as e:
        print(f"Erreur perso_voice_actor pour {row['character']}: {e}")



# # Commit et fermeture
admin_cnx.commit()
admin_cursor.close()
admin_cnx.close()