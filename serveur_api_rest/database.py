import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

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
            charset="utf8mb4"
        )
        return connection
    except Error as e:
        print("Erreur de connexion MySQL:", e)
        return None
