from ..database import get_db_cursor

### --- CREATE ---
def create_genre(data):
    with get_db_cursor() as cursor:
        cursor.execute("INSERT INTO genre (genre) VALUES (%s)", (data.genre,))
        return cursor.lastrowid


### --- READ ---
def get_genre(genre_name):
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM genre WHERE id = %s", (genre_name,))
        return cursor.fetchone()

def get_all_genres():
    with get_db_cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM genre")
        return cursor.fetchall()


### --- UPDATE ---
def update_genre(old_genre, new_genre):
    with get_db_cursor() as cursor:
        cursor.execute("UPDATE genre SET genre = %s WHERE id = %s", (new_genre, old_genre))
        return cursor.rowcount > 0


### --- DELETE ---
def delete_genre(genre_name):
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM genre WHERE id = %s", (genre_name,))
        return cursor.rowcount > 0
