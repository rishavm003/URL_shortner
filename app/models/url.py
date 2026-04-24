from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.session import Base
from pydantic import BaseModel, HttpUrl
from typing import Optional

# SQLAlchemy Model
class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_id = Column(String, unique=True, index=True)
    clicks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Schemas
class URLBase(BaseModel):
    original_url: HttpUrl

class URLCreate(URLBase):
    custom_id: Optional[str] = None

class URLResponse(BaseModel):
    original_url: str
    short_id: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
