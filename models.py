from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


TaskStatus = Literal["todo", "in_progress", "done"]
TaskPriority = Literal["low", "medium", "high"]

class TaskCreate(BaseModel):
  title: str = Field(min_length=1, max_length=50)
  description: str
  status: TaskStatus = 'todo'
  priority: TaskPriority = "low"
  tags: list = [str]
  created_at: date


class Task(TaskCreate):
  id: int

class TaskUpdate(BaseModel):
  model_config = ConfigDict(extra="forbid")
  title: str = Field(min_length=1, max_length=50)
  description: str
  status: TaskStatus = 'todo'
  priority: TaskPriority = "low"
  tags: list = [str]
  created_at: date