import subprocess
import os

scripts = [
    "create_users_sqlite.py",
    "kaggle_to_mongo.py",
    "webscraping.py",
    "webapi_to_mongo.py"
]

for script in scripts:
    script_path = os.path.abspath(script)
    print(f"Running {script_path} ...")
    subprocess.run(["python", script_path], check=True)

print("\nTous les scripts ont été exécutés avec succès !")