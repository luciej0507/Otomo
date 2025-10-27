import sqlite3

DB_PATH = "../data/users.db"

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

# Création utilisateur
def create_user(username: str, password: str, role: str = "user") -> bool:
    """
    Ajoute un utilisateur en SQLite.
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
    
    # sinon on l'ajoute
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    print(f"Utilisateur '{username}' ajouté avec succès.")
    conn.close()
    return True
    
### Boucle pour entrer des utilisateurs depuis le terminal
print("Ajout d'utilisateurs. Tapez 'stop' pour terminer.")
while True:
    username = input("Nom d'utilisateur : ")
    if username.lower() == "stop":
        break
    password = input("mot de passe : ")
    role = input("Rôle (user / admin / contributeur) [défaut: user] : ").strip().lower()
    if role not in ("user", "admin", "contributeur"):
        role = "user"  # valeur par défaut si saisie invalide ou vide
    create_user(username, password, role)

# Affichage des utilisateurs ajoutés
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

print("\n Utilisateurs enregistrés :")
cur.execute("SELECT * FROM users")
for row in cur.fetchall():
    print(row)

# # Fermeture de la connexion
conn.close()