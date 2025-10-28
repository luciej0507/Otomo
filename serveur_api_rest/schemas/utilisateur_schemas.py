from pydantic import BaseModel, Field

class UtilisateurBase(BaseModel):
    identifiant: str
    mdp_hashed: str
    role: str

class UtilisateurCreate(UtilisateurBase):
    pass

class UtilisateurRead(UtilisateurBase):
    id: int

# Pour la connexion
class UtilisateurLogin(BaseModel):
    identifiant: str
    mdp: str     # mot de passe en clair, à vérifier contre le hash