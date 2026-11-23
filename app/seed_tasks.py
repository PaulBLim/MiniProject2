import os
from datetime import date, datetime

from dotenv import load_dotenv
from pymongo import MongoClient

from app.models import Task


load_dotenv()


def seed_tasks() -> None:
    client = MongoClient(
        os.getenv("MONGODB_URI", "mongodb://localhost:27017/"),
        serverSelectionTimeoutMS=5000,
    )
    tasks_collection = client["task_manager"]["tasks"]
    tasks = [
        Task(
            id=1,
            title="Buy groceries",
            description="Buy groceries for the week",
            status="done",
            priority="high",
            tags=["shopping", "important"],
            created_at=date.today(),
        ),
        Task(
            id=2,
            title="Buy Clothes",
            description="Buy new Winter Clothes",
            status="in_progress",
            priority="low",
            tags=["shopping"],
            created_at=date(2026, 2, 22),
        ),
        Task(
            id=3,
            title="Buy Shoes",
            description="Buy new Winter Shoes",
            status="in_progress",
            priority="medium",
            tags=["shopping"],
            created_at=date(2025, 10, 22),
        ),
        Task(
            id=4,
            title="Buy Laptop",
            description="Buy new Laptop for coding",
            status="todo",
            priority="medium",
            tags=["shopping", "important", "coding"],
            created_at=date(2026, 9, 12),
        ),
        Task(
            id=5,
            title="Buy New Phone",
            description="Buy new Phone for communication",
            status="done",
            priority="medium",
            tags=["shopping"],
            created_at=date(2023, 11, 30),
        ),
        Task(
            id=6,
            title="Finish working on House Project",
            description="Finish working on House Project",
            status="todo",
            priority="medium",
            tags=["house", "important", "project", "improvements"],
            created_at=date(2024, 4, 22),
        ),
    ]

    client.admin.command("ping")
    for task in tasks:
        document = task.model_dump()
        document["_id"] = task.id
        document["created_at"] = datetime.combine(task.created_at, datetime.min.time())
        tasks_collection.replace_one({"_id": task.id}, document, upsert=True)

    highest_id = max(task.id for task in tasks)
    client["task_manager"]["counters"].update_one(
        {"_id": "task_id"},
        {"$max": {"seq": highest_id}},
        upsert=True,
    )

    print(f"Seeded {len(tasks)} tasks into task_manager.tasks")
    client.close()


if __name__ == "__main__":
    seed_tasks()
