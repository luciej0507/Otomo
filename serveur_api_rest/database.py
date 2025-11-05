import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from contextlib import contextmanager

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_ROOT = os.getenv("DB_ROOT")
DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_connection():
    try:
        connection = mysql.connector.connect(
            host= DB_HOST,
            user=DB_ROOT,           
            password=DB_ROOT_PASSWORD,   
            database=DB_NAME,   
            charset="utf8mb4",
            autocommit=False,
            pool_name="otomo_pool",     # active le pooling (pour réutiliser les connexions)
            pool_size=10,               # jusqu'à 10 connexions réutilisables en même temps
            pool_reset_session=True     # nettoie la session avant de réutiliser la connexion du pool
        )
        return connection
    except Error as e:
        print("Erreur de connexion MySQL:", e)
        return None

@contextmanager             # garantit qu'une ressource sera toujours nettoyée après utilisation
def get_db_cursor(dictionary=False):
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=dictionary)
        yield cursor
        conn.commit()       # commit automatique
    except Exception:
        conn.rollback()     # annule en cas d'erreur
        raise
    finally:                # ferme proprement les durseur et la connexion quoiqu'il arrive
        if cursor:
            cursor.close()
        if conn:
            conn.close()