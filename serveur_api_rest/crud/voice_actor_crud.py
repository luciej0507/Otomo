from ..database import get_connection

### --- CREATE ---
def create_voice_actor(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO voice_actor (nom_va, url_profil) VALUES (%s, %s)",
                   (data.nom_va, data.url_profil))
    conn.commit()
    return cursor.lastrowid


### --- READ ---
def get_voice_actor(voice_actor_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM voice_actor WHERE id = %s", (voice_actor_id,))
    return cursor.fetchone()

def get_all_voice_actors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM voice_actor")
    return cursor.fetchall()


### --- UPDATE ---
def update_voice_actor(voice_actor_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE voice_actor SET nom_va = %s, url_profil = %s WHERE id = %s",
                   (data.nom_va, data.url_profil, voice_actor_id))
    conn.commit()
    return cursor.rowcount > 0


### --- DELETE ---
def delete_voice_actor(voice_actor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM voice_actor WHERE id = %s", (voice_actor_id,))
    conn.commit()
    return cursor.rowcount > 0
