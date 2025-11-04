from pydantic import BaseModel
from typing import Optional

class CitationBase(BaseModel):
    citation: str
    anime: int                          # anime_id
    personnage: Optional[int] = None    # personnage_id

class CitationCreate(CitationBase):
    pass

class CitationRead(CitationBase):
    id: int
