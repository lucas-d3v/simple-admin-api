from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    role: str = "user"

class Package(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    package_id: int
    version: str
    filename: str
    filepath: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow())