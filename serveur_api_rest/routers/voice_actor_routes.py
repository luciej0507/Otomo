from fastapi import APIRouter, HTTPException, status
from serveur_api_rest.schemas.voice_actor_schemas import VoiceActorCreate, VoiceActorRead
from serveur_api_rest.crud.voice_actor_crud import create_voice_actor, get_voice_actor, get_all_voice_actors, update_voice_actor, delete_voice_actor

router = APIRouter(tags=["Voice Actors"])


### --- Récupération d'un doubleur par son ID ---
@router.get("/{voice_actor_id}", response_model=VoiceActorRead)
def read(voice_actor_id: int):
    va = get_voice_actor(voice_actor_id)
    if not va:
        raise HTTPException(status_code=404, detail="Voice actor non trouvé")
    return va

### --- Récupération de tous les doubleurs ---
@router.get("/", response_model=list[VoiceActorRead])
def read_all():
    return get_all_voice_actors()
