from datetime import date, datetime
import os 
from app.contracts import TaskRepository
from app.models import TaskCreate, TaskStatus, TaskUpdate, Task, TaskPriority, Tittle
from pymongo import MongoClient, ReturnDocument
from dotenv import load_dotenv
from typing import Any
load_dotenv()

def _clean(document: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(document)
    cleaned.pop("_id", None)
    return cleaned

def _to_task(document: dict[str, Any]) -> Task:
    return Task(**_clean(document))

class MongoTaskRepository(TaskRepository):
  def __init__(self, url: str | None = None):
    self.client = MongoClient(url or os.getenv("MONGODB_URI", "mongodb://localhost:27017/"),
    serverSelectionTimeoutMS=5000,
    )
    self.db = self.client["task_manager"]
    self.tasks_collection = self.db["tasks"]
    self.counters = self.db["counters"]

  def _next_task_id(self) -> int:
    if self.counters.find_one({"_id": "task_id"}) is None:
      highest = self.tasks_collection.find_one(sort=[("_id", -1)])
      start = highest["_id"] if highest and isinstance(highest.get("_id"), int) else 0
      self.counters.update_one(
        {"_id": "task_id"},
        {"$setOnInsert": {"seq": start}},
        upsert=True,
      )
    counter = self.counters.find_one_and_update(
      {"_id": "task_id"},
      {"$inc": {"seq": 1}},
      return_document=ReturnDocument.AFTER,
    )
    return counter["seq"]

  def get_task_by_id(self, id: int) -> Task:
    document = self.tasks_collection.find_one({"_id": id})
    return _to_task(document) if document else None

  def create_task(self, task: TaskCreate) -> Task:
    new_id = self._next_task_id()
    document = task.model_dump()
    document["id"] = new_id
    document["_id"] = new_id
    document["created_at"] = datetime.combine(task.created_at, datetime.min.time())
    self.tasks_collection.insert_one(document)
    return Task(id=new_id, **task.model_dump())

  def get_tasks(self, status: TaskStatus | None = None, priority: TaskPriority | None = None, tag: str | None = None, search: str | None = None) -> list[Task]:
      query = {}
      if status:
        query["status"] = status
      if priority:
        query["priority"] = priority
      if tag:
        query["tags"] = tag
      if search:
        query["$or"] = [
          {"title": {"$regex": search, "$options": "i"}},
          {"description": {"$regex": search, "$options": "i"}},
          {"tags": {"$regex": search, "$options": "i"}},
        ]
      return [_clean(task) for task in self.tasks_collection.find(query).sort("_id", 1)]

  def delete_task(self, id: int) -> bool:
    result = self.tasks_collection.delete_one({"_id": id})
    return result.deleted_count > 0

  def delete_task_by_title(self, title: Tittle) -> None:
    result = self.tasks_collection.delete_one({"title": title})
    return result.deleted_count > 0

  def update_task(self, id: int, task_update: TaskUpdate) -> Task | bool:
    created_at = task_update.created_at if task_update.created_at is not None else date.today()
    created_at = datetime.combine(created_at, datetime.min.time())
    replacement = task_update.model_dump(exclude_unset=True, exclude_none=True)
    updated = self.tasks_collection.find_one_and_update({"_id": id}, {"$set": replacement}, return_document=ReturnDocument.AFTER)
    return _to_task(updated) if updated is not None else False
    

  