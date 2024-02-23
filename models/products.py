from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Product(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str] = None
    price: float
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
