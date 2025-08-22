from datetime import datetime
from typing import Optional
from ..utils import enum
from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[enum.PriorityEnum] = None
    category: Optional[enum.CategoryEnum] = None
    due_date: Optional[datetime] = None
    recurrence: Optional[enum.RecurrenceEnum] = None
    completed: Optional[bool] = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    priority: Optional[enum.PriorityEnum] = None
    category: Optional[enum.CategoryEnum] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence: Optional[enum.RecurrenceEnum] = None
    completed: Optional[bool] = None


class TodoOut(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


