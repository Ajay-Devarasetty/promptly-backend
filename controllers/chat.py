from fastapi.concurrency import run_in_threadpool
from models.chat import Chat
from database.db_connection import db
from bson import ObjectId
from datetime import datetime
from groq import Groq
import os
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
  # Secure this!

chat_collection = db["chats"]

def generate_answer(question: str) -> str:
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": question}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    answer = ""
    for chunk in completion:
        answer += chunk.choices[0].delta.content or ""
    return answer

async def save_chat(chat: Chat):
    chat_dict = chat.dict()
    print("chat ",chat_dict)
    # Convert user_id string to ObjectId for MongoDB
    try:
        chat_dict["user_id"] = ObjectId(chat.user_id)
    except Exception:
        raise ValueError("Invalid user_id format")

    chat_dict["timestamp"] = datetime.utcnow()

    # Generate answer in a thread pool (blocking operation)
    answer = await run_in_threadpool(generate_answer, chat.question)
    chat_dict["answer"] = answer
    print("answer", answer)

    # Insert into MongoDB
    result = chat_collection.insert_one(chat_dict)

    # Fetch the inserted document to include all saved fields
    saved_doc = chat_collection.find_one({"_id": result.inserted_id})

    # Convert ObjectId fields to strings for JSON serialization
    saved_doc["id"] = str(saved_doc["_id"])
    saved_doc["user_id"] = str(saved_doc["user_id"])
    del saved_doc["_id"]

    return {"message": "Chat saved successfully", "chat": saved_doc, "success": True }


#-----------------------------------------------------------------------------------------------------------------

def get_chats_by_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid user_id")

    user_obj_id = ObjectId(user_id)
    chats_cursor = chat_collection.find({"user_id": user_obj_id}).sort("timestamp", -1)
    chats = []
    for chat in chats_cursor:
        chat["id"] = str(chat["_id"])
        del chat["_id"]
        chat["user_id"] = str(chat["user_id"])
        chats.append(chat)
    return chats
