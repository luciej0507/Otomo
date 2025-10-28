from ..database import get_connection

### --- CREATE ---
def create_citation(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO citation (citation, anime, personnage) VALUES (%s, %s, %s)",
                   (data.citation, data.anime, data.personnage))
    conn.commit()
    return cursor.lastrowid


### --- READ ---
def get_citation(citation_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM citation WHERE id = %s", (citation_id,))
    return cursor.fetchone()

def get_all_citations():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM citation")
    return cursor.fetchall()


### --- UPDATE ---
def update_citation(citation_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE citation SET citation = %s, anime = %s, personnage = %s WHERE id = %s",
                   (data.citation, data.anime, data.personnage, citation_id))
    conn.commit()
    return cursor.rowcount > 0


### --- DELETE ---
def delete_citation(citation_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM citation WHERE id = %s", (citation_id,))
    conn.commit()
    return cursor.rowcount > 0
