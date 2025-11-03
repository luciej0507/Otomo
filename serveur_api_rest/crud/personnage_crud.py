from ..database import get_db_cursor

### --- CREATE ---
def create_personnage(data):
    with get_db_cursor() as cursor:
        cursor.execute("INSERT INTO personnage (nom_perso) VALUES (%s)", (data.nom_perso,))
        return cursor.lastrowid


### --- READ ---
def get_personnage(personnage_id):
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM personnage WHERE id = %s", (personnage_id,))
        return cursor.fetchone()

def get_all_personnages():
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM personnage")
        return cursor.fetchall()


### --- UPDATE ---
def update_personnage(personnage_id, data):
    with get_db_cursor() as cursor:
        cursor.execute("UPDATE personnage SET nom_perso = %s WHERE id = %s", (data.nom_perso, personnage_id))
        return cursor.rowcount > 0


### --- DELETE ---
def delete_personnage(personnage_id):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM personnage WHERE id = %s", (personnage_id,))
        return cursor.rowcount > 0
