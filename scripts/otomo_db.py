from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

load_dotenv()

DB_HOST      = os.getenv("DB_HOST")
DB_ROOT      = os.getenv("DB_ROOT")
DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
DB_NAME      = os.getenv("DB_NAME")
DB_USER      = os.getenv("DB_USER")
DB_PASSWORD  = os.getenv("DB_PASSWORD")


def main():
    try:
        # Connexion en admin pour créer la base et l'utilisateur
        admin_cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_ROOT,
            password=DB_ROOT_PASSWORD
        )
        admin_cursor = admin_cnx.cursor()

        # Création de la base
        admin_cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            + "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        print(f"Base `{DB_NAME}` créée ou déjà existante.")

        # Création de l'utilisateur et attribution des droits
        admin_cursor.execute(
            f"CREATE USER IF NOT EXISTS '{DB_USER}'@'%' "
            f"IDENTIFIED BY '{DB_PASSWORD}'"
        )
        admin_cursor.execute(
            f"GRANT ALL PRIVILEGES ON `{DB_NAME}`.* "
            f"TO '{DB_USER}'@'%'"
        )
        admin_cursor.execute("FLUSH PRIVILEGES")
        admin_cnx.commit()
        admin_cursor.close()
        admin_cnx.close()
        print(f"Utilisateur `{DB_USER}`@`%` créé/mis à jour.")

    except Error as err:
        print(f"[Erreur admin] {err}")
        return
    
    try:
        # Connexion en tant que nouvel utilisateur sur la DB créée
        user_cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        user_cursor = user_cnx.cursor()

        # Création des tables
        statements = [
            # Table genre
            """
            CREATE TABLE IF NOT EXISTS genre (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                genre TEXT NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table demographic
            """
            CREATE TABLE IF NOT EXISTS demographic (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nom_demo TEXT NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table studio
            """
            CREATE TABLE IF NOT EXISTS studio (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nom_studio VARCHAR(20) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table auteur
            """
            CREATE TABLE IF NOT EXISTS auteur (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                prenom VARCHAR(20) NOT NULL,
                nom VARCHAR(20) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table hobby
            """
            CREATE TABLE IF NOT EXISTS hobby (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nom_hobby VARCHAR(20) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table utilisateur
            """
            CREATE TABLE IF NOT EXISTS utilisateur (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                identifiant VARCHAR(20) NOT NULL,
                mdp VARCHAR(20) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table oeuvre
            """
            CREATE TABLE IF NOT EXISTS oeuvre (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                titre VARCHAR(20) NOT NULL,
                statut VARCHAR(20) NOT NULL,
                hobby INT NOT NULL,
                genre INT NOT NULL,
                demographic INT NOT NULL,
                actif BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (hobby) REFERENCES hobby(id),
                FOREIGN KEY (genre) REFERENCES genre(id),
                FOREIGN KEY (demographic) REFERENCES demographic(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table anime
            """
            CREATE TABLE IF NOT EXISTS anime (
                oeuvre INT NOT NULL,
                studio INT NOT NULL,
                annee_debut VARCHAR(20) NOT NULL,
                annee_fin VARCHAR(20) NOT NULL,
                nombre_episode INT NOT NULL,
                FOREIGN KEY (oeuvre) REFERENCES oeuvre(id),
                FOREIGN KEY (studio) REFERENCES studio(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table manga
            """
            CREATE TABLE IF NOT EXISTS manga (
                oeuvre INT NOT NULL,
                auteur INT NOT NULL,
                annee_debut VARCHAR(20) NOT NULL,
                annee_fin VARCHAR(20) NOT NULL,
                nombre_volume INT NOT NULL,
                FOREIGN KEY (oeuvre) REFERENCES oeuvre(id),
                FOREIGN KEY (auteur) REFERENCES auteur(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table suivi
            """
            CREATE TABLE IF NOT EXISTS suivi (
                utilisateur INT NOT NULL PRIMARY KEY,
                oeuvre INT NOT NULL,
                episodes_vus INT DEFAULT 0,
                volumes_lus INT DEFAULT 0,
                FOREIGN KEY (utilisateur) REFERENCES utilisateur(id),
                FOREIGN KEY (oeuvre) REFERENCES oeuvre(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table de liaison utilisateur_hobby
            """
            CREATE TABLE IF NOT EXISTS utilisateur_hobby (
                utilisateur INT NOT NULL PRIMARY KEY,
                hobby INT NOT NULL,
                FOREIGN KEY (utilisateur) REFERENCES utilisateur(id),
                FOREIGN KEY (hobby) REFERENCES hobby(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        ]

        for stmt in statements:
            user_cursor.execute(stmt)
            print("→ OK :", stmt.strip().split()[2])

        user_cnx.commit()
        user_cursor.close()
        user_cnx.close()
        print("Initialisation de la base terminée avec succès.")

    except Error as err:
        print(f"[Erreur user] {err}")

if __name__ == "__main__":
    main()