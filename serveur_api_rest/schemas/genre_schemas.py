from pydantic import BaseModel

class GenreBase(BaseModel):
    genre: str
    url_genre: str

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id: int
