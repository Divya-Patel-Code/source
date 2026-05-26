from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from application.core.config import settings
from application.utils.exceptions import AppException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

        user_id = payload.get("user_id")
        if not user_id:
            raise AppException("Invalid token: User ID missing", 401)

        return payload

    except ExpiredSignatureError:
        raise AppException("Token has expired", 401)
    except JWTError:
        raise AppException("Invalid or missing credentials", 401)
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e), 500)