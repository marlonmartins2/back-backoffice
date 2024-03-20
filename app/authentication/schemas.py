from pydantic import BaseModel

class SignInModel(BaseModel):
    """
    Schema for the login request

    :param BaseModel: Pydantic base model
    """
    username: str
    password: str
