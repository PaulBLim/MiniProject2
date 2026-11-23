from abc import ABC, abstractmethod
from app.models import Task, Tittle, TaskStatus, TaskPriority

class TaskRepository(ABC):
  @abstractmethod
  def create_task(self, task: Task) -> Task:
    raise NotImplementedError

  @abstractmethod
  def get_task_by_id(self, id: int) -> Task:
    raise NotImplementedError

  @abstractmethod
  def update_task(self, id: int, task: Task) -> Task:
    raise NotImplementedError

  @abstractmethod
  def delete_task(self, id: int) -> None:
    raise NotImplementedError

  @abstractmethod
  def delete_task_by_title(self, title: Tittle) -> None:
    raise NotImplementedError

  @abstractmethod
  def get_tasks(self, status: TaskStatus | None = None, priority: TaskPriority | None = None, tag: str | None = None, search: str | None = None) -> list[Task]:
    raise NotImplementedError