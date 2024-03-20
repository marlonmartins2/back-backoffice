import jwt

from datetime import datetime, timedelta

from passlib.context import CryptContext

from fastapi import HTTPException, status, Security, Depends
from fastapi.routing import APIRoute
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from settings import settings


def verify_password(plain_password, hashed_password):
    """
    Verify the password provided by the user with the hashed password in the database

    :param plain_password: the password provided by the user
    :param hashed_password: the hashed password in the database
    """
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return password_context.verify(plain_password, hashed_password)


def set_password_hash(password):
    """
    Set the password hash for the user

    :param password: the password to be hashed
    """
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return password_context.hash(password)


class Authorize:
    """
    A class to authorize the user to access the application
    """
    @classmethod
    def create_access_token(self, data):
        """
        Create an access token for the user to use for authentication

        :param data: the user data to be encoded in the token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt


    @classmethod
    def create_refresh_token(self, data):
        """
        Create a refresh token for the user to use for authentication

        :param data: the user data to be encoded in the token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt


    @classmethod
    def decode_token(self, token):
        """
        Decode the token to get the user data

        :param token: the token to be decoded
        """
        try:
            context = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return context

        except jwt.ExpiredSignatureError as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Token") from error
        except jwt.InvalidTokenError as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token") from error
        

    @classmethod
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        """
        A wrapper to authenticate the user and decode the token
        """
        return self.decode_token(auth.credentials)


class AuthenticatedRoute(APIRoute):
    """
    A class to authenticate the user before accessing the route

    :param APIRoute: the route to be authenticated
    """
    def __init__(self, *args, **kwargs):
        dependencies = list(kwargs.pop("dependencies", []))
        dependencies.insert(0, Depends(Authorize.auth_wrapper))
        kwargs["dependencies"] = dependencies
        super(AuthenticatedRoute, self).__init__(*args, **kwargs)
