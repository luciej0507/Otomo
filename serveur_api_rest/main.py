from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from serveur_api_rest.routers import (
    anime_routes, anime_routes_secure, utilisateur_routes_secure, personnage_routes, 
    voice_actor_routes, genre_routes, studio_routes, citation_routes, citation_routes_secure,
    suivi_anime_routes, suivi_anime_routes_secure, auth_routes
)

# Point d'entrée
app = FastAPI()

# Inclusion des routes
app.include_router(auth_routes.router)
app.include_router(anime_routes.router, prefix="/anime")
app.include_router(anime_routes_secure.router, prefix="/anime_secure")
app.include_router(utilisateur_routes_secure.router, prefix="/utilisateur")
app.include_router(personnage_routes.router, prefix="/personnage")
app.include_router(voice_actor_routes.router, prefix="/voice_actor")
app.include_router(genre_routes.router, prefix="/genre")
app.include_router(studio_routes.router, prefix="/studio")
app.include_router(citation_routes.router, prefix="/citation")
app.include_router(citation_routes_secure.router, prefix="/citation_secure")
app.include_router(suivi_anime_routes.router, prefix="/suivi")
app.include_router(suivi_anime_routes_secure.router, prefix="/suivi_secure")


# Route racine (route default masqué dans Swagger)
@app.get("/", include_in_schema=False)
def root():
    return {"message": "Bienvenue sur l'API du Projet Otomo"}

# Personnalisation de la documentation OpenAPI
def custom_openapi():
    if app.openapi_schema:          # si le schéma OpenAPI est déjà généré
        return app.openapi_schema   # on le retourne directement
    openapi_schema = get_openapi(   # on crée un schéma OpenAPI personnalisé
        title="API Projet Otomo",
        version="0.1.0",
        description="""
    Cette API permet de gérer :
    - Les animés, personnages, studios, genres et citations.
    - Le suivi des animés pour chaque utilisateur.
    - Des routes sécurisées nécessitant une authentification.
    
    Utiliser le bouton Authorize pour tester les routes protégées.
    """,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {     # permet d'utiliser le bouton Authorize pour tester les routes sécurisées
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Activation du schéma personnalisé
app.openapi = custom_openapi