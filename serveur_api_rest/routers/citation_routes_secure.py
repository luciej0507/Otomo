from fastapi import APIRouter, Depends, status
from serveur_api_rest.schemas.citation_schemas import CitationCreate, CitationRead
from serveur_api_rest.crud.citation_crud import create_citation, get_citation, update_citation, delete_citation
from serveur_api_rest.auth import require_role


router = APIRouter(tags=["Citations (accès sécurisé)"])


### --- Création d'une nouvelle citation ---
@router.post("/", response_model=CitationRead, status_code=status.HTTP_201_CREATED)
def create(data: CitationCreate, user=Depends(require_role(["admin"]))):
    cid = create_citation(data)
    return get_citation(cid)


### --- Mise à jour d'une citation existante ---
@router.put("/{citation_id}", response_model=bool)
def update(citation_id: int, data: CitationCreate, user=Depends(require_role(["admin", "contributeur"]))):
    return update_citation(citation_id, data)


### --- Suppression d'une citation ---
@router.delete("/{citation_id}", response_model=bool)
def delete(citation_id: int, user=Depends(require_role(["admin"]))):
    return delete_citation(citation_id)