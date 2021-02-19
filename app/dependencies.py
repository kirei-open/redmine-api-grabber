from fastapi import Header, HTTPException, status
from jose import JWTError, jwt

async def get_token_header(x_token: str = Header(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(x_token, get_settings().secret_key, algorithms=[get_settings().algorithm])
        username: str = payload.get("username")
        if not username:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception

from app.main import get_settings