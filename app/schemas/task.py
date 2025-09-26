from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = Field(ge=1, le=3)
    due_date: datetime

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=3)
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None

class TaskOut(TaskCreate):
    id: int
    completed: bool

    class Config:
        from_attributes = True
