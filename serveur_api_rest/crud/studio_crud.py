from ..database import get_db_cursor

### --- CREATE ---
def create_studio(data):
    with get_db_cursor() as cursor:
        cursor.execute("INSERT INTO studio (studio) VALUES (%s)", (data.nom,))
        return cursor.lastrowid


### --- READ ---
def get_studio(studio_id):
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM studio WHERE id = %s", (studio_id,))
        return cursor.fetchone()

def get_all_studios():
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM studio")
        return cursor.fetchall()


### --- UPDATE ---
def update_studio(studio_id, data):
    with get_db_cursor() as cursor:
        cursor.execute("UPDATE studio SET studio = %s WHERE id = %s", (data.nom, studio_id))
        return cursor.rowcount > 0


### --- DELETE ---
def delete_studio(studio_id):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM studio WHERE id = %s", (studio_id,))
        return cursor.rowcount > 0
