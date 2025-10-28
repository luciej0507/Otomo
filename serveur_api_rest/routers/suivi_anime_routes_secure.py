from fastapi import APIRouter, HTTPException, Depends, status
from serveur_api_rest.schemas.suivi_anime_schemas import SuiviAnimeCreate, SuiviAnimeRead
from serveur_api_rest.crud.suivi_anime_crud import create_suivi, get_suivi, get_all_suivis, update_suivi, delete_suivi
from serveur_api_rest.auth import require_role


router = APIRouter(tags=["Suivi des animés (accès sécurisé)"])

### --- Création d'un suivi d'animé pour un utilisateur ---
@router.post("/", response_model=SuiviAnimeRead, status_code=status.HTTP_201_CREATED)
def create(data: SuiviAnimeCreate, user=Depends(require_role(["admin"]))):
    suivi_id = create_suivi(data)
    return get_suivi(suivi_id)


### Récupération de tous les suivis ---
@router.get("/", response_model=list[SuiviAnimeRead])
def read_all(user=Depends(require_role(["admin"]))):
    return get_all_suivis()


### --- Mise à jour d'un suivi existant ---
@router.put("/{id}", response_model=bool)
def update(utilisateur_id: int, anime_id: int, data: SuiviAnimeCreate, user=Depends(require_role(["admin", "contributeur"]))):
    return update_suivi(utilisateur_id, anime_id, data)


### --- Suppression d'un suivi ---
@router.delete("/{id}", response_model=bool)
def delete(utilisateur_id: int, anime_id: int, user=Depends(require_role(["admin"]))):
    return delete_suivi(utilisateur_id, anime_id)
