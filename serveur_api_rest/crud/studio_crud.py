from ..database import get_connection

### --- CREATE ---
def create_studio(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO studio (studio) VALUES (%s)", (data.nom,))
    conn.commit()
    return cursor.lastrowid


### --- READ ---
def get_studio(studio_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM studio WHERE id = %s", (studio_id,))
    return cursor.fetchone()

def get_all_studios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM studio")
    return cursor.fetchall()


### --- UPDATE ---
def update_studio(studio_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE studio SET studio = %s WHERE id = %s", (data.nom, studio_id))
    conn.commit()
    return cursor.rowcount > 0


### --- DELETE ---
def delete_studio(studio_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM studio WHERE id = %s", (studio_id,))
    conn.commit()
    return cursor.rowcount > 0
