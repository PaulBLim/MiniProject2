from datetime import date
from pydantic import BaseModel, Field
from typing import Literal


class TaskCreate(BaseModel):
  "title": str = Field(min_length=1, max_length=50)
  "description": str
  "status": Literal["todo" | "in_progress" | "done"] = 'todo'
  "priority": Literal["low" | "medium" | "high"] = "low"
  "tags": list = [str]
  "created_at": date
