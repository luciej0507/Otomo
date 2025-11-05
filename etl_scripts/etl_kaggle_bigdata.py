from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pandas as pd
import ast                      # Pour convertir des chaînes en objets Python (ex: listes)
import mysql.connector
import json

# Charger les variables d'environnement
load_dotenv()

# Connexion à MongoDB
MDB_CONNECTION = os.getenv("MDB_CONNECTION")
MDB_BASE = os.getenv("MDB_BASE")
MDB_COLLECTION = os.getenv("MDB_COLLECTION")

client = MongoClient(MDB_CONNECTION)
db = client[MDB_BASE]
collection = db[MDB_COLLECTION]


# Connexion à MySQL
DB_HOST = os.getenv("DB_HOST")
DB_ROOT = os.getenv("DB_ROOT")
DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

admin_cnx = mysql.connector.connect(
    host=DB_HOST,
    user=DB_ROOT,      
    password=DB_ROOT_PASSWORD,
    database=DB_NAME
)

admin_cursor = admin_cnx.cursor()


# Chemins relatifs pour les 2 fichiers JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

streaming_path = os.path.join(DATA_DIR, "streaming_links_all.json")
genres_path = os.path.join(DATA_DIR, "genres_anime.json")




### --- EXTRACTION ---
cursor = collection.find({"type": "tv"})    # Extraction des documents de type "tv" (animé)
docs = list(cursor)                         # Conversion du cursor en liste de dictionnaires
df = pd.DataFrame(docs)                     # Chargement des données dans un DataFrame pandas



### --- TRANSFORMATION ---
## Suppression des colonnes qui ne seront pas utilisées
colonnes_a_supprimer = [
    "_id", "scored_by", "start_date", "source", "members", "favorites", "episode_duration", 
    "total_duration", "rating", "sfw", "approved", "created_at", "updated_at", "start_season", "real_start_date",
    "real_end_date", "broadcast_day", "broadcast_time", "themes", "demographics", "producers",
    "licensors", "background", "url", "trailer_url", "title_japanese", "title_synonyms"
]

df.drop(columns=colonnes_a_supprimer, inplace=True, errors="ignore")


## Nettoyage et sélection des 300 animés les mieux notés (=les plus populaires)
# Nettoyage de la colonne "score"
# print("Avant :", len(df))
df["score"] = df["score"].astype(str).str.strip()               # on supprime les espaces autour
df["score"] = df["score"].str.replace(",", ".", regex=False)    # on remplace les virgules par des points
df["score"] = df["score"].replace(["--", "?", "N/A", "nan", ""], None)      # on supprime les valeurs non numériques
df["score"] = df["score"].str.replace(r"^0(\d+\.\d+)$", r"\1", regex=True)  # on corrige les scores commençant par un zéro inutile
df["score"] = pd.to_numeric(df["score"], errors="coerce")   # on convertit la colonne "score" en colonne numérique (type float64)
df = df.dropna(subset=["score"])                            # on enleve toutes les lignes qui n’ont pas de score valide
# print("Après :", len(df))

# on définit une variable réprésentant le nombre d'animés à garder (ici 300)
nbr_max = 300
# Sélection des 300 meilleurs animés
df_top = df.sort_values(by="score", ascending=False).head(nbr_max)


"""
## Détection des valeurs manquantes pour chaque colonne 
print("\nValeurs manquantes par colonne :")
print(df_top.isna().sum())
# Résultats : 37 données manquantes
# colonne episodes = 2
# colonne end_date = 10
# colonne title_english = 25

# données manquantes pour la colonnes épisodes : éventuellement à enrichir avec API Jikan
# pour les colonnes end_date et title_english : laisser vide 
# car cela correspond à des animés en cours et dont le titre n'a pas encore été traduit en anglais

# Récupération des anime_id pour les 2 animés sans épisodes renseignés
# missing_episodes = df_top[df_top["episodes"].isna()]
# print("\nAnimés avec 'episodes' manquant :")
# print(missing_episodes[["anime_id", "title"]])
# anime_id : 21 > One Piece
# anime_id : 235 > Detective Conan
"""


## Récupération de l'année dans la colonne "end_date" (ex : "2010-07-04")
# Convertion de la colonne en datetime (on ignore les erreurs si certaines valeurs sont NaN)
df_top["end_date"] = pd.to_datetime(df_top["end_date"], errors="coerce")

# Crée une colonne 'end_year' avec juste l’année
df_top["end_year"] = df_top["end_date"].dt.year

# conversion en entier (car type : object)
df_top["end_year"] = df_top["end_year"].astype("Int64")  # type nullable pour garder les NaN

# même chose pour la colonne "start_year" (car type : float64)
df_top["start_year"] = df_top["start_year"].astype("Int64") 


## Extraction des genres et studios uniques
# Création de 2 nouvelles colonnes avec les genres et les studios convertis en listes
df_top["genres_list"] = df_top["genres"].apply(ast.literal_eval)
df_top["studios_list"] = df_top["studios"].apply(ast.literal_eval)

# Création d'un set pour éviter les doublons
all_genres = set()
all_studios = set()

# Parcours chaque liste de genres
for genre_list in df_top["genres_list"]:
    for genre in genre_list:
        all_genres.add(genre)

# Parcours chaque liste de studios
for studio_list in df_top["studios_list"]:
    for studio in studio_list:
        all_studios.add(studio)

# Tri des genres et des studios pour les afficher proprement
unique_genres = sorted(list(all_genres))
unique_studios = sorted(list(all_studios))

# Vérification 
# Afficher la liste finale
# print("\nGenres uniques trouvés :")
# print(unique_genres)
# print(len(unique_genres))
# print("\nStudios uniques trouvés :")
# print(unique_studios)
# print(len(unique_studios))



## Ajout des plateformes de streaming pour les 300 animés 
# Chargement du fichier JSON contenant
with open(streaming_path, "r", encoding="utf-8") as f:
    streaming_data = json.load(f)

# on récupère les plateformes de streaming associées à un animé donné
def get_platforms(anime_id):        
    anime_id_str = str(anime_id)
    if anime_id_str in streaming_data:
        platforms = [entry["name"] for entry in streaming_data[anime_id_str]]
        return platforms if platforms else None
    return None

# Ajout de la colonne
df_top["streaming_platforms"] = df_top["anime_id"].apply(get_platforms)

# print(df_top.drop(columns=["end_date", "genres_list", "studios_list"]).iloc[0].to_string())
# print(df_top[["anime_id", "streaming_platforms"]].head(10))


## Ajout des urls des genres pour les 300 animés
# Chargement du fichier JSON 
with open(genres_path, "r", encoding="utf-8") as f:
    genres_json = json.load(f)

# Création d’un mapping genre > url
genre_url_map = {entry["name"]: entry["url"] for entry in genres_json["data"]}

# Extraire tous les genres uniques
unique_genres = set()
for genre_list in df_top["genres_list"]:
    unique_genres.update(genre_list)

# Liste des genres avec leur URL
genre_table = []

for genre in sorted(unique_genres):
    url = genre_url_map.get(genre, None)
    genre_table.append({
        "name": genre,
        "url": url
    })

# Conversion en DataFrame
df_genres = pd.DataFrame(genre_table)
# print(df_genres)



## --- CHARGEMENT ---
# Table GENRE
for genre, url in df_genres[["name", "url"]].itertuples(index=False):
    admin_cursor.execute(
        "INSERT INTO genre (genre, url_genre) VALUES (%s, %s)", (genre, url)
    )

## Table STUDIO
for studio in unique_studios:
    admin_cursor.execute(
        "INSERT INTO studio (studio) VALUES (%s)", (studio,)
    )

## Table ANIME
# Convertion de la colonne studio en liste
df_top["studios_list"] = df_top["studios"].apply(ast.literal_eval)

# Récupération des id des studios depuis la base
# Création du mapping
admin_cursor.execute("SELECT id, studio FROM studio")
studio_rows = admin_cursor.fetchall()                           # on récupère tous les résultats de la requête sous forme (id, studio_name)
studio_name_to_id = {name: id_ for id_, name in studio_rows}    # on crée un dictionnaire

# Ajout de studio_id au df_top
df_top["studio_id"] = df_top["studios_list"].apply(
    lambda lst: studio_name_to_id.get(lst[0]) if lst else None
)

df_top["studio_id"] = df_top["studio_id"].astype('Int64')


anime = df_top[[
    'anime_id','title', 'status','episodes', 'start_year', 'synopsis',
    'main_picture', 'title_english', 'end_year', 'studio_id', 'score',
    'streaming_platforms'
    ]]

for row in anime.itertuples(index=False):
    anime_id = int(row.anime_id)
    titre_original = str(row.title)
    titre_anglais = str(row.title_english) if row.title_english else None
    statut = str(row.status)
    score = float(row.score) if not pd.isna(row.score) else None
    annee_debut = int(row.start_year) if not pd.isna(row.start_year) else None
    annee_fin = int(row.end_year) if not pd.isna(row.end_year) else None
    nombre_episodes = int(row.episodes) if not pd.isna(row.episodes) else None
    synopsis = str(row.synopsis) if row.synopsis else None
    studio = int(row.studio_id) if not pd.isna(row.studio_id) else None
    url_image = str(row.main_picture) if row.main_picture else None

    # Conversion des listes python en chaîne lisible
    streaming = (
    ", ".join(row.streaming_platforms)
    if row.streaming_platforms
    else None
)


    admin_cursor.execute(
        """
        INSERT INTO anime (
            anime_id, titre_original, titre_anglais, statut, score,
            annee_debut, annee_fin, nombre_episodes, synopsis,
            studio, url_image, streaming
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            anime_id, titre_original, titre_anglais, statut, score,
            annee_debut, annee_fin, nombre_episodes, synopsis,
            studio, url_image, streaming
        )
    )


## Table de liaison anime_genre
admin_cursor.execute("SELECT id, anime_id FROM anime")
anime_rows = admin_cursor.fetchall()
# Création du mapping entre id de MAL et id SQL
mal_to_sql_id = {}        # dictionnaire vide qui servira de correspondance entre les deux identifiants
for row in anime_rows:
    sql_id = row[0]       # id SQL généré automatiquement
    mal_id = row[1]       # id de MyAnimeList
    mal_to_sql_id[mal_id] = sql_id  # clé = mal_id, valeur = sql_id

admin_cursor.execute("SELECT id, genre FROM genre")
genre_rows = admin_cursor.fetchall()
genre_name_to_id = {name: id_ for id_, name in genre_rows}  # dictionnaire de correspondance entre le nom d’un genre d’anime et son identifiant SQL

for row in df_top.itertuples(index=False):
    mal_id = int(row.anime_id)              # on récupère id MyAnimeList
    sql_id = mal_to_sql_id.get(mal_id)      # on utilise le dictionnaire mal_to_sql_id pour retrouver l’identifiant SQL correspondant à mal_id
    if not sql_id:
        continue

    for genre in row.genres_list:               # on arcourt la liste des genres associés à l'anime
        genre_id = genre_name_to_id.get(genre)  # on utilise le dictionnaire genre_name_to_id pour retrouver l’identifiant SQL du genre
        if genre_id:
            admin_cursor.execute(
                "INSERT INTO anime_genre (anime, genre) VALUES (%s, %s)",
                (sql_id, genre_id)
            )



## Commit et fermeture
admin_cnx.commit()
admin_cursor.close()
admin_cnx.close()



### --- EXPORT DES IDs DES 300 ANIMES SELECTIONNES ---
## Récupération des anime_id pour de futurs appel à l'API Jikan
# Sélection uniquement des colonnes anime_id et title
df_jikan = df_top[["anime_id", "title"]]
## Sauvegarde dans un nouveau fichier CSV
df_jikan.to_csv("anime_jikan_list.csv", index=False)
print("\nFichier 'anime_jikan_list.csv' créé avec succès !")
### ----





