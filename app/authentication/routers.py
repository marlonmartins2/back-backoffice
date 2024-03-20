from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from authentication import SignInModel

from users.models import Users


auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: SignInModel):
    has_user = Users.find_one({"username": data.username}, {"_id": 0})

    if not has_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is incorrect, please try again.",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                "message": "Login successful",
                "access_token": "access_token",
                "refresh_token": "refresh_token",
            }
        ),
    )
