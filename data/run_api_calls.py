import subprocess
import os

# Pour les 300 animés sélectionnés
scripts = [
    "webapi_to_mongo.py",       # récupérer les personnages et doubleurs + ajout dans la base mongdb (collection "characters")
    "streaming_links_jikan.py"  # récupérer les plateformes de streaming
]

for script in scripts:
    script_path = os.path.abspath(script)
    print(f"Running {script_path} ...")
    subprocess.run(["python", script_path], check=True)

print("\nTous les scripts ont été exécutés avec succès !")