from ..database import get_connection

### --- CREATE ---
def create_genre(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO genre (genre) VALUES (%s)", (data.genre,))
    conn.commit()
    return cursor.lastrowid


### --- READ ---
def get_genre(genre_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM genre WHERE id = %s", (genre_name,))
    return cursor.fetchone()

def get_all_genres():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM genre")
    return cursor.fetchall()


### --- UPDATE ---
def update_genre(old_genre, new_genre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE genre SET genre = %s WHERE id = %s", (new_genre, old_genre))
    conn.commit()
    return cursor.rowcount > 0


### --- DELETE ---
def delete_genre(genre_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM genre WHERE id = %s", (genre_name,))
    conn.commit()
    return cursor.rowcount > 0
