#users.py for users routes

from fastapi import APIRouter, HTTPException
from models import UserInfo
from database import user_collection
from bson import ObjectId

router = APIRouter()

@router.post("/users")
async def create_user(user: UserInfo):
    result = await user_collection.insert_one(user.model_dump())
    return {"inserted_id": str(result.inserted_id)}

@router.get("/users")
async def get_all_users():
    users = []
    async for user in user_collection.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users

@router.get("/users/{user_id}")
async def get_user_by_id(user_id: str):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return user

@router.put("/users/{user_id}")
async def update_user_by_id(user_id: str, updated_user: UserInfo):
    result = await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": updated_user.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}
