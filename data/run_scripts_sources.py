import subprocess
import os

scripts = [
    "create_users_sqlite.py",   # création de la base SQLite (et insertion des utilistateurs fictifs depuis le terminal)
    "webscraping.py",           # webscraping
    "kaggle_to_mongo.py",       # transfert du fichier csv dans la base mongo "anime", collection "anime_kaggle"
    "jikan_anime_genres.py",    # récupération de tous les genres/thèmes des animés (grâce à l'API Jikan)
]

# Pour chaque script dans la liste 'scripts'
for script in scripts:
    script_path = os.path.abspath(script)               # on récupère le chemin absolu du script
    print(f"Running {script_path} ...")
    subprocess.run(["python", script_path], check=True) # on exécute le script avec Python, et 'check=True' permet de lever une erreur si l'exécution échoue

print("\nTous les scripts ont été exécutés avec succès !")