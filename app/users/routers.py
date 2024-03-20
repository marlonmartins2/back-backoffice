from uuid import uuid4

from datetime import datetime

from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from services.security import set_password_hash

from users.schemas import RegisterUserModel, ReturnRegisterUserModel
from users.models import Users


user_router = APIRouter(prefix="/user", tags=["Users"])


@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ReturnRegisterUserModel)
async def register_user(data: RegisterUserModel):
    """
    ## Register User
    Endpoint to register a new user.

    :param data: users.schemas.RegisterUserModel - The Register user model.\n
    :return: Message - User Registered Successfuly

    ## Request Body
    - **username**: The username of the user.
    - **password**: The password of the user.
    - **confirm_password**: The password confirmation of the user.
    - **email**: The email of the user.
    - **first_name**: The first name of the user.
    - **last_name**: The last name of the user.
    - **cpf**: The CPF of the user.
    - **phone**: The phone of the user.

    ## Responses
    - **200 OK**: Returns a message with the user registered successfuly.
    - **422 Unprocessable Entity**: If any type of error occurs.
    """

    data.password = set_password_hash(data.password)

    payload = data.model_dump()

    payload.pop("confirm_password")

    payload["id"] = str(uuid4())

    payload["created_at"] = datetime.now().isoformat()

    Users.insert_one(payload)
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User Registered Successfuly"})
