from models import TaskCreate, TaskStatus, TaskUpdate, Task, TaskPriority, Tittle
from fastapi import FastAPI, HTTPException, status
from datetime import date
app = FastAPI(title="Task Manager", description="A simple task manager API")

tasks: dict[int, Task] = {}

def seed_tasks() -> None:
    tasks.clear()
    tasks[1] = Task(
        id=1,
        title="Buy groceries",
        description="Buy groceries for the week",
        status="done",
        priority="high",
        tags=["shopping", "important"],
        created_at=date.today(),
    )
    tasks[2] = Task(
        id=2,
        title="Buy Clothes",
        description="Buy new Winter Clothes",
        status="in_progress",
        priority="low",
        tags=["shopping"],
        created_at=date(2026, 2, 22),
    )
    tasks[3] = Task(
        id=3,
        title="Buy Shoes",
        description="Buy new Winter Shoes",
        status="in_progress",
        priority="medium",
        tags=["shopping"],
        created_at=date(2025, 10, 22),
    )
    tasks[4] = Task(
        id=4,
        title="Buy Laptop",
        description="Buy new Laptop for coding",
        status="todo",
        priority="medium",
        tags=["shopping", "important", "coding"],
        created_at=date(2026, 9, 12),
    )
    tasks[5] = Task(
        id=5,
        title="Buy New Phone",
        description="Buy new Phone for communication",
        status="done",
        priority="medium",
        tags=["shopping"],
        created_at=date(2023, 11, 30),
    )
    tasks[6] = Task(
        id=6,
        title="Finish working on House Project",
        description="Finish working on House Project",
        status="todo",
        priority="medium",
        tags=["house", "important", "project", "improvements"],
        created_at=date(2024, 4, 22),
    )

seed_tasks()

@app.post("/tasks", status_code = status.HTTP_201_CREATED)
async def create_task(task: TaskCreate) -> Task:
    new_id = max(tasks, default=0) + 1
    task = Task(id=new_id, **task.model_dump())
    tasks[new_id] = task
    return task


@app.get("/tasks")
async def get_tasks(status: None | TaskStatus = None, priority: None | TaskPriority = None, tag: None | str = None, search: None | str = None) -> list[Task]:
  tag_cleaned = tag.strip().lower() if tag else ""
  search_cleaned = search.strip().lower() if search else ""
  tasks_list = []
  for task in tasks.values():
    if status is not None and task.status != status:
      continue
    if priority is not None and task.priority != priority:
      continue
    if tag_cleaned and tag_cleaned not in {item.lower() for item in task.tags}:
      continue
    if search_cleaned and search_cleaned not in task.title.lower() and search_cleaned not in task.description.lower():
      continue
    tasks_list.append(task)
  return tasks_list

async def get_task_or_404(task_id):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int) -> Task:
  task = await get_task_or_404(task_id)
  return task



@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate) -> Task:
  current = await get_task_or_404(task_id)
  changes = task_update.model_dump(exclude_unset=True, exclude_none=True)
  if "created_at" not in task_update.model_fields_set:
    changes["created_at"] = date.today()
  updated = current.model_copy(update=changes)
  tasks[task_id] = updated
  return updated


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int) -> dict:
  task = await get_task_or_404(task_id)
  tasks.pop(task_id)
  return {"message": "Task deleted successfully", "task": task.title}

@app.delete("/tasks/title/{task_title}")
async def delete_task_by_title(task_title: Tittle) -> dict:
  for task in tasks.values():
    if task.title.lower() == task_title.lower():
      tasks.pop(task.id)
      return {"message": "Task deleted successfully", "task": task.title}
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")