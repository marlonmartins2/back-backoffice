from pydantic import BaseModel, Field, EmailStr, validator

from users.models import Users


class RegisterUserModel(BaseModel):
    """
    Schema for registering a new user

    :param BaseModel: Pydantic BaseModel
    """
    class Config:
        """
        Pydantic configuration
        """
        arbitrary_types_allowed = True

    username: str = Field(..., title="username")
    password: str = Field(..., title="password")
    confirm_password: str = Field(..., title="confirm_password")
    email: EmailStr = Field(..., title="email")
    first_name: str = Field(..., title="first_name")
    last_name: str = Field(..., title="last_name")
    cpf: str = Field(..., title="cpf")
    phone: str = Field(..., title="phone")

    @validator("username")
    def username_exists(cls, username):
        """
        Check if the username already exists in the database

        :param username: Username of the user
        """
        if Users.find_one({"username": username}, {"username": 1}):
            raise ValueError("The username already exists")
        
        return username

    @validator("password")
    def password_complexity(cls, password):
        """
        Check if the password is complex enough

        :param password: Password of the user
        """
        errors = []
        if len(password) < 8:
            errors.append("The password must contain at least 8 characters")
        
        if not any(char.isdigit() for char in password):
            errors.append("The password must contain at least one digit")
        
        if not any(char.isupper() for char in password):
            errors.append("The password must contain at least one uppercase letter")
        
        if not any(char.islower() for char in password):
            errors.append("The password must contain at least one lowercase letter")
        
        if not any(char in ["@", "#", "$", "%", "&", "*", "!", "&"] for char in password):
            errors.append("The password must contain at least one special character")
        
        if errors:
            raise ValueError(", ".join(errors))
        
        return password
        
    @validator("confirm_password")
    def password_confirmation_validation(cls, password_confirmation, values):
        """
        Check if the password confirmation matches the password

        :param password_confirmation: Password confirmation of the user
        """
        if "password" in values and password_confirmation != values["password"]:
            raise ValueError("The passwords does not match")

        return password_confirmation


class ReturnRegisterUserModel(BaseModel):
    """
    Schema for returning a registered user

    :param BaseModel: Pydantic BaseModel
    """
    message: str = "User Registered Successfuly."
