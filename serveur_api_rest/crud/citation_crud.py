from ..database import get_db_cursor

### --- CREATE ---
def create_citation(data):
    with get_db_cursor() as cursor:
        cursor.execute("INSERT INTO citation (citation, anime, personnage) VALUES (%s, %s, %s)",
                        (data.citation, data.anime, data.personnage))
        return cursor.lastrowid


### --- READ ---
def get_citation(citation_id):
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM citation WHERE id = %s", (citation_id,))
        return cursor.fetchone()

def get_all_citations():
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM citation")
        return cursor.fetchall()


### --- UPDATE ---
def update_citation(citation_id, data):
    with get_db_cursor() as cursor:
        cursor.execute("UPDATE citation SET citation = %s, anime = %s, personnage = %s WHERE id = %s",
                        (data.citation, data.anime, data.personnage, citation_id))
        return cursor.rowcount > 0


### --- DELETE ---
def delete_citation(citation_id):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM citation WHERE id = %s", (citation_id,))
        return cursor.rowcount > 0
