from fastapi import APIRouter, HTTPException, status
from serveur_api_rest.schemas.genre_schemas import GenreCreate, GenreRead
from serveur_api_rest.crud.genre_crud import create_genre, get_genre, get_all_genres, update_genre, delete_genre

router = APIRouter(tags=["Genres"])


### --- Récupération d'un genre par son nom ---
@router.get("/{genre}", response_model=GenreRead)
def read(genre: str):
    g = get_genre(genre)
    if not g:
        raise HTTPException(status_code=404, detail="Genre non trouvé")
    return g

### --- Récupération de tous les genres ---
@router.get("/", response_model=list[GenreRead])
def read_all():
    return get_all_genres()