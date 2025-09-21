#database connection database.py

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://vinayhegde0824_db_user:fQi3ySV1LmDvppK6@cluster0.es0bnz7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client["qa_automate"]

user_collection = db["UserInfo"]
item_collection = db["ItemInfo"]
order_collection = db["OrderInfo"]
