from ..database import get_db_cursor

### --- CREATE ---
def create_anime(data):
    with get_db_cursor() as cursor:
        query = """
            INSERT INTO anime (titre_original, titre_anglais, score, nombre_episodes, annee_debut, annee_fin,
                                nombre_episodes_diffuses, studio, url_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data.titre_original, data.titre_anglais, data.score, data.nombre_episodes,
            data.annee_debut, data.annee_fin, data.nombre_episodes_diffuses, data.studio, data.url_image
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
            UPDATE anime SET titre_original=%s, titre_anglais=%s, score=%s, nombre_episodes=%s,
            annee_debut=%s, annee_fin=%s, nombre_episodes_diffuses=%s, studio=%s, url_image=%s
            WHERE id=%s
        """
        cursor.execute(query, (
            data.titre_original, data.titre_anglais, data.score, data.nombre_episodes,
            data.annee_debut, data.annee_fin, data.nombre_episodes_diffuses, data.studio,
            data.url_image, anime_id
        ))
        return cursor.rowcount > 0


### --- DELETE ---
def delete_anime(anime_id):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM anime WHERE id = %s", (anime_id,))
        return cursor.rowcount > 0
