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
            # Table studio
            """
            CREATE TABLE IF NOT EXISTS studio (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                studio VARCHAR(50) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table genre
            """
            CREATE TABLE IF NOT EXISTS genre (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                genre VARCHAR(50) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table voice_actor
            """
            CREATE TABLE IF NOT EXISTS voice_actor (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nom_va VARCHAR(50) NOT NULL,
                url_profil TEXT NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table utilisateur
            """
            CREATE TABLE IF NOT EXISTS utilisateur (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                identifiant VARCHAR(20) NOT NULL,
                mdp_hashed VARCHAR(150) NOT NULL,
                role VARCHAR(20) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table anime
            """
            CREATE TABLE IF NOT EXISTS anime (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                anime_id INT NOT NULL,
                titre_original VARCHAR(100) NOT NULL,
                titre_anglais VARCHAR(100) NOT NULL,
                score VARCHAR(20) NOT NULL,
                statut VARCHAR(20) NOT NULL,
                annee_debut VARCHAR(20) NOT NULL,
                annee_fin VARCHAR(20) NULL,
                nombre_episodes INT NULL,
                synopsis TEXT NOT NULL,
                studio INT NOT NULL,
                url_image VARCHAR(150) NOT NULL,
                FOREIGN KEY (studio) REFERENCES studio(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table personnage
            """
            CREATE TABLE IF NOT EXISTS personnage (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nom_perso VARCHAR(50) NOT NULL,
                role VARCHAR(20) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table citation
            """
            CREATE TABLE IF NOT EXISTS citation (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                citation TEXT NOT NULL,
                anime INT NOT NULL,
                personnage INT NULL,
                FOREIGN KEY (anime) REFERENCES anime(id),
                FOREIGN KEY (personnage) REFERENCES personnage(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table de liaison anime_genre
            """
            CREATE TABLE IF NOT EXISTS anime_genre (
                anime INT NOT NULL,
                genre INT NOT NULL,
                PRIMARY KEY (anime, genre),
                FOREIGN KEY (anime) REFERENCES anime(id),
                FOREIGN KEY (genre) REFERENCES genre(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table de liaison anime_personnage
            """
            CREATE TABLE anime_personnage (
                personnage_id INT NOT NULL,
                anime_id INT NOT NULL,
                PRIMARY KEY (personnage_id, anime_id),
                FOREIGN KEY (personnage_id) REFERENCES personnage(id),
                FOREIGN KEY (anime_id) REFERENCES anime(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table de liaison perso_voice_actor
            """
            CREATE TABLE perso_voice_actor (
                personnage_id INT NOT NULL,
                voice_actor_id INT NOT NULL,
                PRIMARY KEY (personnage_id, voice_actor_id),
                FOREIGN KEY (personnage_id) REFERENCES personnage(id),
                FOREIGN KEY (voice_actor_id) REFERENCES voice_actor(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table de liaison suivi_anime
            """
            CREATE TABLE IF NOT EXISTS suivi_anime (
                utilisateur INT NOT NULL,
                anime INT NOT NULL,
                episodes_vus INT DEFAULT 0,
                statut_suivi ENUM('En cours', 'Terminé', 'À voir'),
                PRIMARY KEY (utilisateur, anime),
                FOREIGN KEY (utilisateur) REFERENCES utilisateur(id),
                FOREIGN KEY (anime) REFERENCES anime(id)
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