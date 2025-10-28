from ..database import get_connection

### --- CREATE ---
def create_anime(data):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO anime (titre_original, titre_anglais, score, nombre_episodes, annee_debut, annee_fin,
                           nombre_episodes_diffuses, studio, url_image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        data.titre_original, data.titre_anglais, data.score, data.nombre_episodes,
        data.annee_debut, data.annee_fin, data.nombre_episodes_diffuses, data.studio, data.url_image
    ))
    conn.commit()
    return cursor.lastrowid


### --- READ ---
def get_anime(anime_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM anime WHERE id = %s", (anime_id,))
    return cursor.fetchone()

def get_all_animes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM anime")
    return cursor.fetchall()


### --- UPDATE ---
def update_anime(anime_id, data):
    conn = get_connection()
    cursor = conn.cursor()
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
    conn.commit()
    return cursor.rowcount > 0


### --- DELETE ---
def delete_anime(anime_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM anime WHERE id = %s", (anime_id,))
    conn.commit()
    return cursor.rowcount > 0
