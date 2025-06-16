from fastapi import HTTPException
import bcrypt
from database.db_connection import db
from models.user import User 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_collection = db["users"]

def create_user(user):
    user_dict = user.dict()

    # Check if user with same email already exists
    existing_user = user_collection.find_one({"email": user_dict["email"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash the password
    plain_password = user_dict["password"]
    hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    user_dict["password"] = hashed_password.decode("utf-8")  # Store as string in DB

    result = user_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    del user_dict["_id"]
    return {"message": "User created", "userDetails": user_dict, "success":True}

#-------------------------------------------------------------------------------------------------------

def login_user(email: str, password: str):
    
    user = user_collection.find_one({"email": email})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = user["password"]

    if not bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Remove internal MongoDB ID for response (optional)
    user["id"] = str(user["_id"])
    del user["_id"]
    del user["password"]  # Don't send hashed password in response

    return {"message": "Login successful", "userDetails": user}
