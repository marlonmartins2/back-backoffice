from uuid import uuid4

from datetime import datetime

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from services.security import set_password_hash, AuthenticatedRoute

from users.models import Users
from users.schemas import RegisterUserModel, ReturnRegisterUserModel, UserModel, UserPatchModel


user_router = APIRouter(prefix="/users", tags=["Users"], route_class=AuthenticatedRoute)


@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ReturnRegisterUserModel, summary="Endpoint to register a new user.")
async def register_user(data: RegisterUserModel):
    """
    # Register User

    :param data: users.schemas.RegisterUserModel - The Register user model.\n
    :return: Message - User Registered Successfuly

    ## Request Body
    - **username**: The username of the user.
    - **password**: The password of the user. Must contain at least 8 characters, one digit, one uppercase letter, one lowercase letter and one special character.
    - **confirm_password**: The password confirmation of the user. Must match the password.
    - **email**: The email of the user.
    - **first_name**: The first name of the user.
    - **last_name**: The last name of the user.
    - **cpf**: The CPF of the user.
    - **phone**: The phone of the user.

    ## Responses
    - **200 OK**: Returns a message the user registered successfuly and user_id.
    - **422 Unprocessable Entity**: If any type of error occurs.
    """

    data.password = set_password_hash(data.password)

    payload = data.model_dump()

    payload.pop("confirm_password")

    payload["id"] = str(uuid4())

    payload["is_active"] = False

    payload["created_at"] = datetime.now().isoformat()

    Users.insert_one(payload)
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "User Registered Successfuly",
            "user_id": payload["id"],
        }
    )


@user_router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserModel], summary="Endpoint to get all users.")
async def get_users():
    """
    # Get Users

    ## Responses
    - **200 OK**: Returns a list of users.
    - **200 OK**: if not users on database to be returned empty array.
    """

    users = Users.find({}, {"_id": 0})

    if not users:
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder([]))

    return_users = [UserModel(**user) for user in users]

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(return_users))


@user_router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserModel, summary="Endpoint to get a user by id.")
async def get_user(user_id: str):
    """
    # Get User

    ## Query Parameters
    - **user_id**: The id from user.

    ## Responses
    - **200 OK**: Returns the user.
    - **404 Not Found**: User Not Found.
    """

    user = Users.find_one({"id": user_id}, {"_id": 0})

    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"User Not Found", "content": {"user_id": user_id}}
        )

    return_user = UserModel(**user)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(return_user))


@user_router.patch("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserModel, summary="Endpoint to update a user by id.")
async def update_user(user_id: str, data: UserPatchModel):
    """
    # Update User

    ## Query Parameters
    - **user_id**: The id from user.

    ## Request Body
    - **username**: The username of the user.
    - **password**: The password of the user.
    - **email**: The email of the user.
    - **first_name**: The first name of the user.
    - **last_name**: The last name of the user.
    - **cpf**: The CPF of the user.
    - **phone**: The phone of the user.

    ## Responses
    - **200 OK**: Returns a message the user updated successfuly and user updated data.
    - **422 Unprocessable Entity**: If any type of error occurs.
    - **404 Not Found**: User Not Found.

    """

    user = Users.find_one({"id": user_id}, {"_id": 0})

    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"User Not Found", "content": {"user_id": user_id}}
        )

    payload = data.model_dump(exclude_unset=True)

    payload["updated_at"] = datetime.now().isoformat()

    user = Users.update_one({"id": user_id}, {"$set": payload})
    
    return_user = UserModel(**user)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "User Updated Successfuly",
            "user": jsonable_encoder(return_user),
        }
    )


@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK, summary="Endpoint to deactivate a user by id.")
async def delete_user(user_id: str):
    """
    # Delete User

    ## Query Parameters
    - **user_id**: The id from user.

    ## Responses
    - **200 OK**: Returns a message the user deactivated successfuly.
    - **404 Not Found**: User Not Found.
    """

    user = Users.find_one({"id": user_id}, {"_id": 0})

    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"User Not Found", "content": {"user_id": user_id}}
        )

    Users.deactivate_one({"id": user_id})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User Deactivated Successfuly"}
    )


@user_router.patch("/{user_id}/activate", status_code=status.HTTP_200_OK, summary="Endpoint to activate a user by id.")
async def activate_user(user_id: str):
    """
    # Activate User

    ## Query Parameters
    - **user_id**: The id from user.

    ## Responses
    - **200 OK**: Returns a message the user activated successfuly.
    - **404 Not Found**: User Not Found.
    """

    user = Users.find_one({"id": user_id}, {"_id": 0})

    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"User Not Found", "content": {"user_id": user_id}}
        )

    Users.activate_one({"id": user_id})

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "User Activated Successfuly"}
    )
