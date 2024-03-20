from pydantic import BaseModel

class SignInModel(BaseModel):
    """
    Schema for the login request

    :param BaseModel: Pydantic base model
    """
    username: str
    password: str


class ReturnLoginModel(BaseModel):
    """
    Schema for the login response

    :param BaseModel: Pydantic base model
    """
    message: str = "Login successful"
    access_token: str
    refresh_token: str
    token_type: str
