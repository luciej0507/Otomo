import subprocess
import os

scripts = [
    "etl_kaggle_bigdata.py",
    "etl_api_jikan.py",
    "etl_webscraping.py",
    "etl_utilisateur.py",
    "etl_fichier_perso.py"
]

for script in scripts:
    script_path = os.path.abspath(script)
    print(f"Running {script_path} ...")
    subprocess.run(["python", script_path], check=True)

print("\nTous les scripts ont été exécutés avec succès !")