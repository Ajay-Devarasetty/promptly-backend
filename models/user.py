from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name : str
    email : EmailStr
    password : str

class LoginRequest(BaseModel):
    email: str
    password: str