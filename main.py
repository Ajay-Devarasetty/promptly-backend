from fastapi import FastAPI

from routes.user import router as user_Router
from routes.chat import router as chat_Router

from dotenv import load_dotenv

load_dotenv()

import os
print(os.getenv("GROQ_API_KEY"))

app = FastAPI()
app.include_router(user_Router)
app.include_router(chat_Router)

from fastapi.middleware.cors import CORSMiddleware


# Allow requests from your frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
