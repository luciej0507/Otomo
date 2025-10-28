from fastapi import APIRouter, HTTPException
from serveur_api_rest.schemas.suivi_anime_schemas import SuiviAnimeRead
from serveur_api_rest.crud.suivi_anime_crud import get_suivi


router = APIRouter(tags=["Suivi des animés"])


### Récupération d'un suivi par l'ID de l'utilisateur ---
@router.get("/{id}", response_model=SuiviAnimeRead)
def read(utilisateur_id: int, anime_id: int):
    suivi = get_suivi(utilisateur_id, anime_id)
    if not suivi:
        raise HTTPException(status_code=404, detail="Suivi non trouvé")
    return suivi
