from pydantic import BaseModel

class StudioBase(BaseModel):
    studio: str

class StudioCreate(StudioBase):
    pass

class StudioRead(StudioBase):
    id: int
