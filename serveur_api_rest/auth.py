from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import bcrypt
from serveur_api_rest.crud.utilisateur_crud import get_utilisateur

load_dotenv()

# Type d'authentification (Token JWT transmis dans le hearder Authorization: Bearer <token>)
security = HTTPBearer()

# Clé secrète, algorithme pour signer le JWT et durée de validité du token
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")  # Valeur par défaut si absent
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))


# Vérification d'un mot de passe en clair contre un mot de passe haché (stocké en base)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# Création d'un token JWT avec l'id et le rôle
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Récupération de l'utilisateur courant depuis le token
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials     # on récupère le token JWT depuis le header Authorization
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])     # on décode le token pour récupérer les données
        user_id = int(payload.get("sub"))                                   # on extrait l'id et le rôle de l'utilisateur
        role = payload.get("role")
        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        return {"id": user_id, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")


# Vérification que l'utilisateur a le rôle requis
def require_role(required_roles: list[str]):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] not in required_roles:
            raise HTTPException(status_code=403, detail="Accès interdit")
        return user
    return role_checker