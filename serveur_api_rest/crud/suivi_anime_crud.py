from ..database import get_db_cursor

### --- CREATE ---
def create_suivi(data):
    with get_db_cursor() as cursor:
        cursor.execute("INSERT INTO suivi_anime (utilisateur, anime, episodes_vus, statut_suivi) VALUES (%s, %s, %s, %s)",
                        (data.utilisateur, data.anime, data.episodes_vus, data.statut_suivi))
        return cursor.lastrowid


### --- READ ---
def get_suivi(utilisateur_id, anime_id):
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM suivi_anime WHERE utilisateur = %s AND anime = %s", (utilisateur_id, anime_id))
        return cursor.fetchone()

def get_all_suivis():
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM suivi_anime")
        return cursor.fetchall()


### --- UPDATE ---
def update_suivi(utilisateur_id, anime_id, data):
    with get_db_cursor() as cursor:
        cursor.execute("UPDATE suivi_anime SET utilisateur = %s, anime = %s, episodes_vus = %s, statut_suivi = %s WHERE utilisateur = %s AND anime = %s",
                        (data.utilisateur, data.anime, data.episodes_vus, data.statut_suivi, utilisateur_id, anime_id))
        return cursor.rowcount > 0


### --- DELETE ---
def delete_suivi(utilisateur_id, anime_id):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM suivi_anime WHERE utilisateur = %s AND anime = %s", (utilisateur_id, anime_id))
        return cursor.rowcount > 0