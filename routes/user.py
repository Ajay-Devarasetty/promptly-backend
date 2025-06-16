from fastapi import APIRouter
from models.user import User, LoginRequest
from controllers.user import create_user, login_user 

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#---------------------------------------------------------------------------------------------------------

@router.post("/saveUser")
def create_User(user : User):
    return create_user(user)

#-----------------------------------------------------------------------------------------------------------

@router.post("/login")
def login(request: LoginRequest):
    return login_user(request.email, request.password)

#------------------------------------------------------------------------------------------------------------