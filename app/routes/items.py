#items.py for items routes

from fastapi import APIRouter, HTTPException
from app.models import ItemInfo
from app.database import item_collection
from bson import ObjectId

router = APIRouter()

@router.post("/items")
async def create_item(item: ItemInfo):
    result = await item_collection.insert_one(item.model_dump())
    return {"inserted_id": str(result.inserted_id)}

@router.get("/items")
async def get_all_items():
    items = []
    async for item in item_collection.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return items

@router.get("/items/{item_id}")
async def get_item_by_id(item_id: str):
    item = await item_collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item["_id"] = str(item["_id"])
    return item

@router.put("/items/{item_id}")
async def update_item_by_id(item_id: str, updated_item: ItemInfo):
    result = await item_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": updated_item.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item updated successfully"}
