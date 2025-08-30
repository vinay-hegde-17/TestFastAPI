#orders.py for orders routes

from fastapi import APIRouter, HTTPException
from models import OrderInfo
from database import order_collection
from bson import ObjectId

router = APIRouter()

@router.post("/orders")
async def create_order(order: OrderInfo):
    result = await order_collection.insert_one(order.model_dump())
    return {"inserted_id": str(result.inserted_id)}

@router.get("/orders")
async def get_all_orders():
    orders = []
    async for order in order_collection.find():
        order["_id"] = str(order["_id"])
        orders.append(order)
    return orders

@router.get("/orders/{order_id}")
async def get_order_by_id(order_id: str):
    order = await order_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["_id"] = str(order["_id"])
    return order

@router.put("/orders/{order_id}")
async def update_order_by_id(order_id: str, updated_order: OrderInfo):
    result = await order_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": updated_order.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order updated successfully"}
