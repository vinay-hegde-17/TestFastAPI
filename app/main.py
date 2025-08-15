#main.py entry point

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes.index import router
from app.database import user_collection, item_collection, order_collection

@asynccontextmanager
async def lifespan(app: FastAPI):
    for col in [user_collection, item_collection, order_collection]:
        await col.insert_one({"_temp": True})
        await col.delete_many({"_temp": True})
    print("✅ Collections ensured.")
    yield
    print("🧹 App shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
