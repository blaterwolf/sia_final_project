from datetime import datetime as dt
from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str
    password: str

# * Schema for request body
# ? Since gumagawa tayo ng user, ang kailangan lang natin na schema is username and password which is provided na sa may UserBase natin. Kung titignan natin yung user_model.User, makikita mo dun na ang kailangan lang natin na mga info username at password since yung UUID automatic na yun and yung dates naman ay nasa baba which is yung User class.


class CreateUser(UserBase):
    pass

# Schema for response body


class User(UserBase):
    created_at: dt
    updated_at: dt
