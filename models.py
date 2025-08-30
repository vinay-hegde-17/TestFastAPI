#Models creation models.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from pydantic import EmailStr

class UserInfo(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    address: str = Field(..., min_length=1)
    phone: str = Field(..., pattern=r'^\d{10}$')  # exactly 10 digits
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ItemInfo(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    price: float = Field(..., gt=0)   # must be > 0
    stock: int = Field(..., ge=0)     # must be >= 0

class OrderInfo(BaseModel):
    user_id: str = Field(..., min_length=1)
    items: List[str] = Field(..., min_items=1)
    total: float = Field(..., gt=0)
    status: str = Field(default="pending")
