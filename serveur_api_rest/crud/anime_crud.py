from ..database import get_db_cursor

### --- CREATE ---
def create_anime(data):
    with get_db_cursor() as cursor:
        query = """
            INSERT INTO anime (anime_id, titre_original, titre_anglais, score, statut, annee_debut, annee_fin,
                                nombre_episodes, synopsis, studio, url_image, streaming)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.anime_id, data.titre_original, data.titre_anglais, data.score, data.statut, data.annee_debut, 
            data.annee_fin, data.nombre_episodes, data.synopsis, data.studio, data.url_image, data.streaming
        ))
        return cursor.lastrowid


### --- READ ---
def get_anime(anime_id):
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM anime WHERE id = %s", (anime_id,))
        return cursor.fetchone()

def get_all_animes():
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM anime")
        return cursor.fetchall()


### --- UPDATE ---
def update_anime(anime_id, data):
    with get_db_cursor() as cursor:
        query = """
            UPDATE anime SET titre_original=%s, titre_anglais=%s, score=%s, statut=%s, annee_debut=%s, 
            annee_fin=%s, nombre_episodes=%s, synopsis=%s, studio=%s, url_image=%s, streaming=%s
            WHERE id=%s
        """
        cursor.execute(query, (
            data.titre_original, data.titre_anglais, data.score, data.statut, data.annee_debut, 
            data.annee_fin, data.nombre_episodes, data.synopsis, data.studio, data.url_image, 
            data.streaming, anime_id
        ))
        return cursor.rowcount > 0


### --- DELETE ---
def delete_anime(anime_id):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM anime WHERE id = %s", (anime_id,))
        return cursor.rowcount > 0
