from models import TaskCreate, TaskUpdate, Task
from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Task Manager", description="A simple task manager API")

tasks: dict[int, Task] = {}


@app.get("/tasks")
async def get_tasks() -> list[Task]:
  return list(tasks.values())

async def get_task_or_404(task_id):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@app.post("/tasks")
async def create_task(task: TaskCreate) -> Task:
    new_id =max(tasks, default=0) + 1
    task = Task(id=new_id, **task.model_dump())
    tasks[new_id] = task
    return task

@app.get("/tasks/{task_id}")
async def get_task(task_id: int) -> Task:
  return tasks[task_id]

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskUpdate) -> Task:
  task = get_task_or_404(task_id)
  task.title = task.title or task.title
  task.description = task.description or task.description
  task.completed = task.completed or task.completed
  return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int) -> dict:
  get_task_or_404(task_id)
  task = tasks.pop(task_id)
  return {"message": "Task deleted successfully", "task": task.title}

@app.delete("/tasks/{task_title}")
async def delete_task_by_title(task_title: str) -> dict:
  for task in tasks.values():
    if task.title == task_title:
      tasks.pop(task.id)
      return {"message": "Task deleted successfully", "task": task.title}
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")