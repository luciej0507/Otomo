from pydantic import BaseModel

class GenreBase(BaseModel):
    genre: str

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id: int
