from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import bcrypt
from serveur_api_rest.crud.utilisateur_crud import get_utilisateur

load_dotenv()

security = HTTPBearer()

# Clé secrète, algorithme pour signer le JWT et durée de validité du token
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")  # Valeur par défaut si absent
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))


# Vérification d'un mot de passe en clair contre un hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# Création d'un token JWT avec l'id et le rôle
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dépendance pour récupérer l'utilisateur courant
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
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