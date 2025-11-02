from dotenv import load_dotenv
import os
import re
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

admin_cursor = admin_cnx.cursor()



### --- EXTRACTION et TRANSFORMATION ---
# Détection des épisodes vus
def extraire_episodes(titre):
    # Formats reconnus
    motifs = [
        r"\((\d+)\s*(eps|episodes?)\)",       # (13 eps)
        r"\(ep(?:isode)?\s*(\d+)\)",          # (ep 13)
        r"\((\d+)\s*ep(?:isode)?s?\)",        # (13 ep)
    ]

    for motif in motifs:
        match = re.search(motif, titre)
        if match:
            return int(match.group(1))
    return None

def nettoyer_titre(titre):
    # Supprime les parenthèses contenant des infos d'épisodes
    titre_sans_parenthese = re.sub(r"\(\s*\d+\s*(eps?|episodes?)\s*\)", "", titre, flags=re.IGNORECASE)
    # Supprime aussi les parenthèses vides ou résiduelles
    titre_sans_parenthese = re.sub(r"\(\s*\)", "", titre_sans_parenthese)
    return titre_sans_parenthese.strip()


def extraire_animes_depuis_txt(fichier_txt):
    with open(fichier_txt, encoding="utf-8") as f:
        lignes = f.readlines()

    lignes[0] = lignes[0].replace('\ufeff', '')

    statut = None
    animes = []

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue

        # Détection des sections
        if "Animés terminés" in ligne:
            statut = "terminé"
            continue
        elif "Animés commencés" in ligne:
            statut = "en cours"
            continue
        elif "Animés à voir" in ligne:
            statut = "à voir"
            continue

        # Extraction des titres
        if ligne.startswith("-"):
            titre = ligne[1:].strip()
        else:
            titre = ligne

        episodes = extraire_episodes(titre)
        titre_nettoye = nettoyer_titre(titre)

        animes.append({
            "titre": titre_nettoye,
            "statut": statut,
            "episodes_vus": episodes
        })

    return animes

animes = extraire_animes_depuis_txt("../data/notes_perso.txt")


## Récupération des titres et ID depuis la table anime
admin_cursor.execute("SELECT id, titre_anglais FROM anime")
anime_db = admin_cursor.fetchall()

# Création d'un dictionnaire de correspondance
anime_dict = {titre.lower().strip(): id for id, titre in anime_db}

# Association titre_nettoye et anime_id
for anime in animes:
    titre = anime["titre"].lower().strip()
    anime_id = anime_dict.get(titre)

    if anime_id:
        anime["anime_id"] = anime_id
    else:
        anime["anime_id"] = None

animes_valides = [a for a in animes if a["anime_id"] is not None]

# --------
# Garder une trace des animés exclus 
# animes_exclus = [a for a in animes if a["anime_id"] is None]
# print("Animés non insérés (pas dans la table anime) :")
# for a in animes_exclus:
#     print("-", a["titre"])
# --------



### --- CHARGEMENT --- 
# Récupération de l'identifiant de l'utilisateur ciblé
admin_cursor.execute("SELECT id FROM utilisateur WHERE identifiant = %s", ("lucie",))
resultat = admin_cursor.fetchone()
id_utilisateur = resultat[0] if resultat else None

# Insertion dans la table suivi_anime
for a in animes_valides:
    admin_cursor.execute("""
        INSERT INTO suivi_anime (utilisateur, anime, episodes_vus, statut_suivi)
        VALUES (%s, %s, %s, %s)
    """, (id_utilisateur, a["anime_id"], a["episodes_vus"], a["statut"]))



# Commit et fermeture
admin_cnx.commit()
admin_cursor.close()
admin_cnx.close()