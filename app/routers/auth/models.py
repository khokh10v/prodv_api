
from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """ Pydantic model for token """
    # по спецификации OAuth2 
    # иначе авторизация из документации FastApi не работает 
    access_token: str 
    token_type: str


class TokenData(BaseModel):
    """ Pydantic model for token data """
    email: Optional[str] = None