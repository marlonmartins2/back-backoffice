from datetime import datetime

from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from services import verify_password, Authorize

from authentication import SignInModel, ReturnLoginModel, ReturnRefreshModel, RefreshModel

from users.models import Users


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=ReturnLoginModel, summary="Endpoint to authenticate the user.")
async def login(data: SignInModel):
    """
    # Login

    ## Request Body
    - **username**: The username of the user.
    - **password**: The password of the user.

    ## Responses
    - **200 OK**: Returns a dictionary containing the JWT token upon successful authentication.
    - **400 Bad Request**: If the user is not found or if the username/password is incorrect.
    - **401 Unauthorized**: If the user is not active.
    """
    user = Users.find_one({"username": data.username}, {"_id": 0})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found, please contact the suport.",
        )
    
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active, please contact the suport.",
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
        "role_id": user["role_id"],
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


@auth_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=ReturnRefreshModel, summary="Endpoint to refresh JWT token.")
async def refresh(data: RefreshModel):
    """
    # Refresh Token

    ## Request Body
    - **refresh_token**: The refresh token.

    ## Responses
    - **200 OK**: Returns a dictionary containing the new JWT token upon successful refresh.
    - **400 Bad Request**: If the refresh token is invalid or expired.
    - **401 Unauthorized**: If the user is not active.
    """
    token_data = Authorize.decode_token(data.refresh_token)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired refresh token, please login again.",
        )
    
    user = Users.find_one({"id": token_data["user_id"]}, {"_id": 0})

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active, please contact the suport.",
        )

    access_token = Authorize.create_access_token(token_data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({"access_token": access_token}),
    )
