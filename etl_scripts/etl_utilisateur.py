from dotenv import load_dotenv
import os
import sqlite3
import pandas as pd
import bcrypt
import mysql.connector

# Charger les variables d'environnement
load_dotenv()

# Connexion MySQL
DB_HOST = os.getenv("DB_HOST")
DB_ROOT = os.getenv("DB_ROOT")
DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# connexion à la base SQL
admin_cnx = mysql.connector.connect(
    host=DB_HOST,
    user=DB_ROOT,      
    password=DB_ROOT_PASSWORD,
    database=DB_NAME
)

admin_cursor = admin_cnx.cursor()


# --- Connexion à la base SQLite et EXTRACTION ---
conn_sqlite = sqlite3.connect("../data/users.db")
df_users = pd.read_sql_query("SELECT * FROM users", conn_sqlite)
conn_sqlite.close()



### --- TRANSFORMATION ---
# Hashage des mots de passe
def hash_password_bcrypt(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()  # Pour l'insérer comme texte dans MySQL

df_users["mdp_hashed"] = df_users["password"].apply(hash_password_bcrypt)
df_users.drop(columns=["password"], inplace=True)


### --- CHARGEMENT ---
# Table UTILISATEUR
# Insertion des données
for _, row in df_users.iterrows():
    admin_cursor.execute("""
        INSERT INTO utilisateur (identifiant, mdp_hashed, role)
        VALUES (%s, %s, %s)
    """, (row["username"], row["mdp_hashed"], row["role"]))


# Commit et fermeture
admin_cnx.commit()
admin_cursor.close()
admin_cnx.close()