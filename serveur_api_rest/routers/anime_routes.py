from fastapi import APIRouter, HTTPException
from serveur_api_rest.schemas.anime_schemas import AnimeRead
from serveur_api_rest.crud.anime_crud import get_anime, get_all_animes


router = APIRouter(tags=["Animés"])


### --- Récupérer tous les animés ---
@router.get(
    "/",
    response_model=list[AnimeRead],
    summary="Liste des animés disponibles",
    description="Retourne tous les animés enregistrés dans la base. Accessible sans authentification."
)
def read_all():
    return get_all_animes()


### --- Récupération d'un animé précis (grâce à son id) ---
# @router.get("/{anime_id}", response_model=AnimeRead)
# def read(anime_id: int):
#     anime = get_anime(anime_id)
#     if not anime:
#         raise HTTPException(status_code=404, detail="Anime not found")
#     return anime