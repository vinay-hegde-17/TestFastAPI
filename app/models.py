#Models creation models.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserInfo(BaseModel):
    name: str
    email: str
    address: str
    phone: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ItemInfo(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class OrderInfo(BaseModel):
    user_id: str
    items: List[str]
    total: float
    status: str = "pending"
