from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBearer
from serveur_api_rest.schemas.utilisateur_schemas import UtilisateurLogin
from serveur_api_rest.crud.utilisateur_crud import get_utilisateur
from serveur_api_rest.auth import create_access_token, verify_password

router = APIRouter(tags=["Authentification"])
security = HTTPBearer()

@router.post("/login")
def login(data: UtilisateurLogin):
    print("Tentative de login :", data.identifiant)
    user = get_utilisateur(data.identifiant)
    print("Utilisateur trouvé :", user)
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur inconnu")

    print("Vérification du mot de passe…")
    if not verify_password(data.mdp, user["mdp_hashed"]):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    token = create_access_token({"sub": str(user["id"]), "role": user["role"]})
    print("Token généré avec succès :", token)
    return {"access_token": token, "token_type": "bearer"}
