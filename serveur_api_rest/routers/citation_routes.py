from fastapi import APIRouter, HTTPException
from serveur_api_rest.schemas.citation_schemas import CitationRead
from serveur_api_rest.crud.citation_crud import get_citation, get_all_citations


router = APIRouter(tags=["Citations"])


### --- Récupération d'une citation par son ID ---
@router.get("/{citation_id}", response_model=CitationRead)
def read(citation_id: int):
    citation = get_citation(citation_id)
    if not citation:
        raise HTTPException(status_code=404, detail="Citation non trouvée")
    return citation

### --- Récupération de toutes les citations ---
@router.get("/", response_model=list[CitationRead])
def read_all():
    return get_all_citations()


