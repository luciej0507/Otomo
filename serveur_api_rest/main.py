from fastapi import FastAPI, HTTPException
from dto.connexion import DataAccess as da

app = FastAPI()
 
@app.get("/") 
def read_root(): 
    return {"message" : "Bienvenue sur Otomo"}

