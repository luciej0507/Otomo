from pydantic import BaseModel
from typing import Optional

class SuiviAnimeBase(BaseModel):
    utilisateur: int  # utilisateur_id
    anime: int        # anime_id
    episodes_vus: Optional[int]
    statut_suivi: str

class SuiviAnimeCreate(SuiviAnimeBase):
    pass

class SuiviAnimeRead(SuiviAnimeBase):
    pass
