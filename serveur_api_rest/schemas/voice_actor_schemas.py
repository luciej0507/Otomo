from pydantic import BaseModel

class VoiceActorBase(BaseModel):
    nom_va: str
    url_profil: str

class VoiceActorCreate(VoiceActorBase):
    pass

class VoiceActorRead(VoiceActorBase):
    id: int
