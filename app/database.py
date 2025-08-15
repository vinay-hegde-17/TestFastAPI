#database connection database.py

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["qa_automate"]

user_collection = db["UserInfo"]
item_collection = db["ItemInfo"]
order_collection = db["OrderInfo"]
