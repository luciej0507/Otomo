from fastapi import APIRouter, HTTPException, Depends, status
from serveur_api_rest.schemas.utilisateur_schemas import UtilisateurCreate, UtilisateurRead
from serveur_api_rest.crud.utilisateur_crud import create_utilisateur, get_utilisateur, get_all_utilisateurs, update_utilisateur, delete_utilisateur
from serveur_api_rest.auth import require_role


router = APIRouter(tags=["Utilisateurs (accès sécurisé)"])

### --- Création d'un nouvel utilisateur ---
@router.post("/", response_model=UtilisateurRead, status_code=status.HTTP_201_CREATED)
def create(data: UtilisateurCreate, user=Depends(require_role(["admin"]))):
    user_id = create_utilisateur(data)
    return get_utilisateur(user_id)

### --- Récupération d'un utilisateur par son ID ---
@router.get("/{id}", response_model=UtilisateurRead)
def read(id: int, user=Depends(require_role(["admin"]))):
    user = get_utilisateur(id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

### --- Récupération de tous les utilisateurs ---
@router.get("/", response_model=list[UtilisateurRead])
def read_all(user=Depends(require_role(["admin"]))):
    return get_all_utilisateurs()

### --- Mise à jour d'un utilisateur existant ---
@router.put("/{id}", response_model=bool)
def update(id: int, data: UtilisateurCreate, user=Depends(require_role(["admin"]))):
    return update_utilisateur(id, data)

### --- Suppression d'un utilisateur
@router.delete("/{id}", response_model=bool)
def delete(id: int, user=Depends(require_role(["admin"]))):
    return delete_utilisateur(id)
