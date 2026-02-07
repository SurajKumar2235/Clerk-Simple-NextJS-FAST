from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base

class User(Base):
    __tablename__ = "users"

    clerk_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="user")
    company_name = Column(String, nullable=True)
    credits = Column(Integer, default=10)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
