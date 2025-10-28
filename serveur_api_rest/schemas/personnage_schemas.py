from pydantic import BaseModel

class PersonnageBase(BaseModel):
    nom_perso: str

class PersonnageCreate(PersonnageBase):
    pass

class PersonnageRead(PersonnageBase):
    id: int
