from ..database import get_db_cursor

### --- CREATE ---
def create_utilisateur(data):
    with get_db_cursor() as cursor:
        query = "INSERT INTO utilisateur (identifiant, mdp_hashed, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (data.identifiant, data.mdp_hashed, data.role))
        return cursor.lastrowid


### --- READ ---
def get_utilisateur(identifiant):
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM utilisateur WHERE identifiant = %s", (identifiant,))
        user = cursor.fetchone()
        return user

def get_all_utilisateurs():
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM utilisateur")
        return cursor.fetchall()


### --- UPDATE ---
def update_utilisateur(id, data):
    with get_db_cursor() as cursor:
        query = "UPDATE utilisateur SET identifiant=%s, mdp_hashed=%s, role=%s WHERE id=%s"
        cursor.execute(query, (data.identifiant, data.mdp_hashed, data.role, id))
        return cursor.rowcount > 0


### --- DELETE ---
def delete_utilisateur(identifiant):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM utilisateur WHERE identifiant = %s", (identifiant,))
        return cursor.rowcount > 0