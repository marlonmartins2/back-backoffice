from datetime import datetime

from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from services import set_password_hash, verify_password, Authorize

from authentication import SignInModel, ReturnLoginModel, ReturnRefreshModel, RefreshModel

from users.models import Users


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=ReturnLoginModel)
async def login(data: SignInModel):
    """
    ## Login
    Endpoint to authenticate users and generate JWT token.

    :param data: authentication.schemas.SignInModel - The user login data.\n
    :return: A dictionary containing the JWT token.

    ## Request Body
    - **username**: The username of the user.
    - **password**: The password of the user.

    ## Responses
    - **200 OK**: Returns a dictionary containing the JWT token upon successful authentication.
    - **400 Bad Request**: If the user is not found or if the username/password is incorrect.
    """
    user = Users.find_one({"username": data.username}, {"_id": 0})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found, please contact the suport.",
        )
    
    if not verify_password(data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is incorrect, please try again.",
        )
    
    token_data = {
        "user_id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
    }

    access_token = Authorize.create_access_token(token_data)

    refresh_token = Authorize.create_refresh_token(token_data)


    Users.update_one(
        {"username": data.username},
        {"$set": {"last_login": datetime.now().isoformat()}},
    )


    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }
        ),
    )


@auth_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=ReturnRefreshModel)
async def refresh(data: RefreshModel):
    """
    ## Refresh Token
    Endpoint to refresh the JWT token.

    :param data: authentication.schemas.RefreshModel - The refresh token.\n
    :return: A dictionary containing the new JWT token.

    ## Request Body
    - **refresh_token**: The refresh token.

    ## Responses
    - **200 OK**: Returns a dictionary containing the new JWT token upon successful refresh.
    - **400 Bad Request**: If the refresh token is invalid or expired.
    """
    token_data = Authorize.decode_token(data.refresh_token)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired refresh token, please login again.",
        )

    access_token = Authorize.create_access_token(token_data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"access_token": access_token}),
    )
