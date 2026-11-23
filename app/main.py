from app.models import TaskCreate, TaskStatus, TaskUpdate, Task, TaskPriority, Tittle
from fastapi import FastAPI, HTTPException, status, Request, Form
from pathlib import Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from app.repository import MongoTaskRepository
from app.contracts import TaskRepository
from app.seed_tasks import seed_tasks

APP_DIR = Path(__file__).parent
PROJECT_ROOT = APP_DIR.parent
templates = Jinja2Templates(directory=APP_DIR / "templates")

app = FastAPI(title="Task Manager", description="A simple task manager API")

repository: TaskRepository = MongoTaskRepository()


app.mount("/static", StaticFiles(directory=PROJECT_ROOT/"static"), name="static")

#seed_tasks()

@app.get("/")
def root():
    return {"message": "Welcome to the Task Manager API"}

@app.get("/", response_class=HTMLResponse)
async def tasks_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="tasks.html",
        context={"tasks": repository.get_tasks()},
    )


@app.post("/tasks", status_code = status.HTTP_201_CREATED)
async def create_task(task: TaskCreate) -> Task:
    return repository.create_task(task)

@app.post("/ui/tasks")
async def create_task_from_form(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()] = "",
    task_status: Annotated[str, Form()] = "todo",
    priority: Annotated[str, Form()] = "low",
    tags: Annotated[str, Form()] = "",
):
    tag_list = [
        tag.strip()
        for tag in tags.split(",")
        if tag.strip()
    ]

    task_data = TaskCreate(
        title=title,
        description=description,
        status=task_status,
        priority=priority,
        tags=tag_list,
    )

    await create_task(task_data)

    return RedirectResponse(url="/", status_code=303)


@app.get("/tasks")
async def get_tasks(status: None | TaskStatus = None, priority: None | TaskPriority = None, tag: None | str = None, search: None | str = None) -> list[Task]:
  return repository.get_tasks(status, priority, tag, search)


@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int) -> Task:
  task = repository.get_task_by_id(task_id)
  if not task:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
  return task



@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate) -> Task:
  updated_task = repository.update_task(task_id, task_update)
  if not updated_task:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
  return updated_task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int) -> dict:
  matches = repository.get_task_by_id(task_id)
  if not matches:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
  repository.delete_task(task_id)
  return {"message": "Task deleted successfully", "task": matches.title}

@app.delete("/tasks/title/{task_title}")
async def delete_task_by_title(task_title: Tittle) -> dict:
  if not repository.delete_task_by_title(task_title):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
  return {"message": "Task deleted successfully", "task": task_title}