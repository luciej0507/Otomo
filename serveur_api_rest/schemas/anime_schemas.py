from pydantic import BaseModel
from typing import Optional


class AnimeBase(BaseModel):
    anime_id: int
    titre_original: str
    titre_anglais: Optional[str] = None
    score: Optional[float] = None
    statut: Optional[str] = None
    annee_debut: Optional[int] = None
    annee_fin: Optional[int] = None
    nombre_episodes: Optional[int] = None
    synopsis: Optional[str] = None
    studio: Optional[int] = None
    url_image: Optional[str] = None
    streaming: Optional[str] = None


# Modèle utilisé pour les requêtes POST (création d’un anime)
class AnimeCreate(AnimeBase):
    pass

# Modèle utilisé pour les réponses envoyées au client (lecture d'un animé en base)
class AnimeRead(AnimeBase):
    id: int

# Modèle pour les mises à jour (requête PUT)
class AnimeUpdate(BaseModel):
    titre_original: Optional[str] = None
    titre_anglais: Optional[str] = None
    score: Optional[float] = None
    statut: Optional[str] = None
    annee_debut: Optional[int] = None
    annee_fin: Optional[int] = None
    nombre_episodes: Optional[int] = None
    synopsis: Optional[str] = None
    studio: Optional[int] = None
    url_image: Optional[str] = None
    streaming: Optional[str] = None
