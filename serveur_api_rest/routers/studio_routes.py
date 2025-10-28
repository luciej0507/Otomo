from fastapi import APIRouter, HTTPException, status
from serveur_api_rest.schemas.studio_schemas import StudioCreate, StudioRead
from serveur_api_rest.crud.studio_crud import create_studio, get_studio, get_all_studios, update_studio, delete_studio

router = APIRouter(tags=["Studios"])


### --- Récupération d'un studio par son ID ---
@router.get("/{studio_id}", response_model=StudioRead)
def read(studio_id: int):
    studio = get_studio(studio_id)
    if not studio:
        raise HTTPException(status_code=404, detail="Studio non trouvé")
    return studio

### --- Récupération de tous les studios ---
@router.get("/", response_model=list[StudioRead])
def read_all():
    return get_all_studios()
