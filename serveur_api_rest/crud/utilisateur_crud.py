from ..database import get_connection

### --- CREATE ---
def create_utilisateur(data):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO utilisateur (identifiant, mdp_hashed, role) VALUES (%s, %s, %s)"
    cursor.execute(query, (data.identifiant, data.mdp_hashed, data.role))
    conn.commit()
    return cursor.lastrowid


### --- READ ---
def get_utilisateur(identifiant):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM utilisateur WHERE identifiant = %s", (identifiant,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_all_utilisateurs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM utilisateur")
    return cursor.fetchall()


### --- UPDATE ---
def update_utilisateur(id, data):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE utilisateur SET identifiant=%s, mdp_hashed=%s, role=%s WHERE id=%s"
    cursor.execute(query, (data.identifiant, data.mdp_hashed, data.role, id))
    conn.commit()
    return cursor.rowcount > 0


### --- DELETE ---
def delete_utilisateur(identifiant):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM utilisateur WHERE identifiant = %s", (identifiant,))
    conn.commit()
    return cursor.rowcount > 0