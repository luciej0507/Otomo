import mysql.connector
from mysql.connector import Error
from dto.config import DB_HOST, DB_ROOT, DB_ROOT_PASSWORD, DB_NAME

class DataAccess:

    @classmethod
    def connexion(cls):
        try:
            cls.conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_ROOT,
                password=DB_ROOT_PASSWORD,
                database=DB_NAME
            )
            cls.cursor = cls.conn.cursor(dictionary=True)
        except Error as e:
            print(f"Erreur de connexion : {e}")
    
    @classmethod
    def deconnexion(cls):
        if cls.cursor:
            cls.cursor.close()
        if cls.conn:
            cls.conn.close()

    @classmethod
    def get_utilisateurs(cls):
        