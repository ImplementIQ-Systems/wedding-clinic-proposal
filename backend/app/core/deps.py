from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError as JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db

bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    from app.models.user import User

    try:
        data = decode_token(credentials.credentials)
        if data.get("type") != "access":
            raise ValueError("not an access token")
        user_id = int(data["sub"])
    except (JWTError, ValueError, KeyError):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Utilizador não encontrado")
    return user
