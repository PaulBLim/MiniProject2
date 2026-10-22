from models import TaskCreate, TaskStatus, TaskUpdate, Task, TaskPriority
from fastapi import FastAPI, HTTPException, status
from datetime import date
app = FastAPI(title="Task Manager", description="A simple task manager API")

tasks: dict[int, Task] = {}

def seed_tasks() -> None:
    global tasks 
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
        created_at=date(2026, 10, 22),
    )
    tasks[3] = Task(
        id=3,
        title="Buy Shoes",
        description="Buy new Winter Shoes",
        status="in_progress",
        priority="medium",
        tags=["shopping"],
        created_at=date(2026, 10, 22),
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
        created_at=date(2026, 10, 30),
    )
    tasks[6] = Task(
        id=6,
        title="Finish working on House Project",
        description="Finish working on House Project",
        status="todo",
        priority="medium",
        tags=["house", "important", "project", "improvements"],
        created_at=date(2026, 10, 22),
    )

seed_tasks()


# @app.get("/tasks")
# async def get_tasks() -> list[Task]:
#   return list(tasks.values())

async def get_task_or_404(task_id):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@app.post("/tasks")
async def create_task(task: TaskCreate) -> Task:
    new_id = max(tasks, default=0) + 1
    task = Task(id=new_id, **task.model_dump())
    tasks[new_id] = task
    return task

@app.get("/tasks/{task_id}")
async def get_task(task_id: int) -> Task:
  task = await get_task_or_404(task_id)
  return task

@app.get("/tasks")
async def read_task(status: TaskStatus = 'done', priority: TaskPriority = 'high', tags: str | None = None, q: str | None = None) -> list[Task]:
  tasks_list = []
  for task in tasks.values():
    if status and task.status != status:
      continue
    if priority and task.priority != priority:
      continue
    if tags and tags not in task.tags:
      continue
    if q and q not in task.title and q not in task.description:
      continue
    tasks_list.append(task)
  return tasks_list

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskUpdate) -> Task:
  task = await get_task_or_404(task_id)
  task.title = task.title or task.title
  task.description = task.description or task.description
  task.completed = task.completed or task.completed
  return task

# @app.delete("/tasks/{task_id}")
# async def delete_task(task_id: int) -> dict:
#   await get_task_or_404(task_id)
#   task = tasks.pop(task_id)
#   return {"message": "Task deleted successfully", "task": task.title}

@app.delete("/tasks/{task_title}")
async def delete_task_by_title(task_title: str) -> dict:
  for task in tasks.values():
    if task.title.lower() == task_title.lower():
      tasks.pop(task.id)
      return {"message": "Task deleted successfully", "task": task.title}
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")