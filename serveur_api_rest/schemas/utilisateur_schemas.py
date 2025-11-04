from pydantic import BaseModel, Field

class UtilisateurBase(BaseModel):
    identifiant: str
    mdp: str     # mot de passe en clair envoyé par l'utilisateur
    role: str

class UtilisateurCreate(UtilisateurBase):
    pass

class UtilisateurRead(BaseModel):   # dissociation modèle entrée et sortie pour ne pas afficher le mdp
    id: int
    identifiant: str
    role: str
# ne pas inclure les mots de passse dans les nodèles de réponses

# Pour la connexion
class UtilisateurLogin(BaseModel):
    identifiant: str
    mdp: str     # mot de passe en clair, à vérifier contre le hash