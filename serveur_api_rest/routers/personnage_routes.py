from fastapi import APIRouter, HTTPException, status
from serveur_api_rest.schemas.personnage_schemas import PersonnageCreate, PersonnageRead
from serveur_api_rest.crud.personnage_crud import create_personnage, get_personnage, get_all_personnages, update_personnage, delete_personnage

router = APIRouter(tags=["Personnages"])


### --- Récupération d'un personnage par son ID ---
@router.get("/{personnage_id}", response_model=PersonnageRead)
def read(personnage_id: int):
    perso = get_personnage(personnage_id)
    if not perso:
        raise HTTPException(status_code=404, detail="Personnage non trouvé")
    return perso

### --- Récupération de tous les personnages ---
@router.get("/", response_model=list[PersonnageRead])
def read_all():
    return get_all_personnages()
