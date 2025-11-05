import sqlite3

DB_PATH = "../data/users.db"    # Chemin vers le fichier de la base SQLite

# Création de la table users avec rôles
"""
Initialise la base SQLite (crée la table users si elle n'existe pas).
"""
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('user', 'admin', 'contributeur')) DEFAULT 'user'
    )
''')
conn.commit()
conn.close()

# Création des utilisateurs
def create_user(username: str, password: str, role: str = "user") -> bool:
    """
    Ajoute un utilisateur dans la base SQLite.
    Retourne False si l'utilisateur existe déjà.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Vérifier d'abord si le username existe déjà
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    if cur.fetchone():
        print(f"Utilisateur '{username}' existe déjà.")
        conn.close()
        return False
    
    # si non, ajouter l'utilisateur avec son rôle
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    print(f"Utilisateur '{username}' ajouté avec succès.")
    conn.close()
    return True
    

### --- Saisie des utilisateur via le terminal ---
print("Ajout d'utilisateurs. Tapez 'stop' pour terminer.")
while True:
    username = input("Nom d'utilisateur : ")
    if username.lower() == "stop":
        break
    password = input("mot de passe : ")
    role = input("Rôle (user / admin / contributeur) [défaut: user] : ").strip().lower()

    # Si le rôle est invalide ou vide, on met 'user' par défaut
    if role not in ("user", "admin", "contributeur"):
        role = "user"  

    # Appelle la fonction pour créer l'utilisateur
    create_user(username, password, role)

# Connexion à la base pour lire les données
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("\n Utilisateurs enregistrés :")
cur.execute("SELECT * FROM users")      # repère tous les utilisateurs
for row in cur.fetchall():
    print(row)

# Fermeture de la connexion
conn.close()