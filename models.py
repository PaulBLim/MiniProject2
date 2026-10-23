from datetime import date
from pydantic import BaseModel, Field, ConfigDict, AfterValidator
from typing import Literal, Annotated


TaskStatus = Literal["todo", "in_progress", "done"]
TaskPriority = Literal["low", "medium", "high"]

def title_validator(title: str) -> str:
  title = title.strip()
  if not title:
    raise ValueError("Title cannot be empty")
  return title

Tittle = Annotated[str, Field(min_length=1, max_length=50), AfterValidator(title_validator)]

class TaskCreate(BaseModel):
  title: Tittle
  description: str
  status: TaskStatus = 'todo'
  priority: TaskPriority = "low"
  tags: list = []
  created_at: date = Field(default_factory=date.today)


class Task(TaskCreate):
  id: int

class TaskUpdate(BaseModel):
  model_config = ConfigDict(extra="forbid")
  title: Tittle | None = None
  status: TaskStatus | None = None
  priority: TaskPriority | None = None
  tags: list | None = None
  created_at: date | None = None