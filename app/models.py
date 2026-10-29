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

def date_validator(date: date) -> date:
  if date > date.today():
    raise ValueError("Date cannot be in the future")
  return date

Tittle = Annotated[str, Field(min_length=1, max_length=50), AfterValidator(title_validator)]
Date = Annotated[date, AfterValidator(date_validator)]
Description = Annotated[str, Field( max_length=200)]
class TaskCreate(BaseModel):
  title: Tittle
  description: Description = ""
  status: TaskStatus = 'todo'
  priority: TaskPriority = "low"
  tags: list = []
  created_at: Date = Field(default_factory=date.today)


class Task(TaskCreate):
  id: int

class TaskUpdate(BaseModel):
  model_config = ConfigDict(extra="forbid")
  title: Tittle | None = None
  description: Description | None = None
  status: TaskStatus | None = None
  priority: TaskPriority | None = None
  tags: list | None = None
  created_at: Date | None = None