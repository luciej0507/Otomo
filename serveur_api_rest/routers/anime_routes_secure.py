from fastapi import APIRouter, HTTPException, Depends, status
from serveur_api_rest.schemas.anime_schemas import AnimeCreate, AnimeRead
from serveur_api_rest.crud.anime_crud import create_anime, get_anime, update_anime, delete_anime
from serveur_api_rest.auth import require_role


router = APIRouter(tags=["Animés (accès sécurisés)"])

### POUR TESTER LES AUTHENTIFICATIONS DANS SWAGGER
### ROUTE A SUPPRIMER QUAND TEST FINIS
### --- Récupération d'un animé précis (grâce à son id) ---
@router.get("/{anime_id}", response_model=AnimeRead)
def read(anime_id: int, user=Depends(require_role(["admin"]))):
    anime = get_anime(anime_id)
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    return anime
# -------------------------------------------


### --- Création d'un animé ---
@router.post("/", response_model=AnimeRead, status_code=status.HTTP_201_CREATED)
def create(data: AnimeCreate, user=Depends(require_role(["admin"]))):
    anime_id = create_anime(data)
    return get_anime(anime_id)


### --- Mise à jour d'un animé ---
@router.put("/{anime_id}", response_model=bool)
def update(anime_id: int, data: AnimeCreate, user=Depends(require_role(["admin", "contributeur"]))):
    return update_anime(anime_id, data)


### --- Suppression d'un animé ---
@router.delete("/{anime_id}", response_model=bool)
def delete(anime_id: int, user=Depends(require_role(["admin"]))):
    return delete_anime(anime_id)
