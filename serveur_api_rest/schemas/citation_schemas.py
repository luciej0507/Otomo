from pydantic import BaseModel

class CitationBase(BaseModel):
    citation: str
    anime: int       # anime_id
    personnage: int  # personnage_id

class CitationCreate(CitationBase):
    pass

class CitationRead(CitationBase):
    id: int
