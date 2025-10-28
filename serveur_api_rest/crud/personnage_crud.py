from ..database import get_connection

### --- CREATE ---
def create_personnage(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO personnage (nom_perso) VALUES (%s)", (data.nom_perso,))
    conn.commit()
    return cursor.lastrowid


### --- READ ---
def get_personnage(personnage_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personnage WHERE id = %s", (personnage_id,))
    return cursor.fetchone()

def get_all_personnages():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personnage")
    return cursor.fetchall()


### --- UPDATE ---
def update_personnage(personnage_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE personnage SET nom_perso = %s WHERE id = %s", (data.nom_perso, personnage_id))
    conn.commit()
    return cursor.rowcount > 0


### --- DELETE ---
def delete_personnage(personnage_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personnage WHERE id = %s", (personnage_id,))
    conn.commit()
    return cursor.rowcount > 0
