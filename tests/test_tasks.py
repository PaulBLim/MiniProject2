from main import TaskCreate
from pydantic import ValidationError
import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from main import app
from models import TaskUpdate
import main

client = TestClient(app)

class Test_task_create :
    def test_create_task(self):
        task = TaskCreate(title="Test Task", description="Test Description")
        assert task.title == "Test Task"
        assert task.description == "Test Description"

    def test_create_task_with_empty_title(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="", description="Test Description")

    def test_create_task_with_empty_description(self):
        task = TaskCreate(title="Test Task", description="")
        assert task.description == ""

    def test_create_task_with_long_description(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="Test Task", description="A" * 201)

    def test_create_task_with_long_title(self):
        with pytest.raises(ValidationError):
            TaskCreate(title="A" * 51, description="Test Description")

    def test_default_values(self):
        task = TaskCreate(title="Test Task")
        assert task.description == ""
        assert task.status == "todo"
        assert task.priority == "low"
        assert task.tags == []
        assert task.created_at == date.today()

class Test_task_update :
    def test_update_task(self):
        task = TaskUpdate(title="Updated Task", description="Updated Description", status="in_progress", priority="medium", tags=["test"], created_at=date.today()- timedelta(days=4) )
        assert task.title == "Updated Task"
        assert task.description == "Updated Description"
        assert task.status == "in_progress"
        assert task.priority == "medium"
        assert task.tags == ["test"]
        assert task.created_at == date.today()- timedelta(days=4)

    def test_update_task_with_empty_title(self):
        with pytest.raises(ValidationError):
            TaskUpdate(title="", description="Test Description")

    def test_update_task_with_empty_description(self):
        task = TaskUpdate(title="Test Task", description="")
        assert task.description == ""
    
    def test_update_task_with_long_description(self):
        with pytest.raises(ValidationError):
            TaskUpdate(title="Test Task", description="A" * 201)

    def test_update_task_with_long_title(self):
        with pytest.raises(ValidationError):
            TaskUpdate(title="A" * 51, description="Test Description")

    def test_update_task_with_default_values(self):
        task = TaskUpdate(title="Test Task")
        assert task.title == "Test Task"
        assert task.description == None
        assert task.status == None
        assert task.priority == None
        assert task.tags == None
        assert task.created_at == None


    def test_update_task_with_invalid_status(self):
        with pytest.raises(ValidationError):
            TaskUpdate(title="Test Task", description="Test Description", status="invalid")

    def test_update_task_with_invalid_priority(self):
        with pytest.raises(ValidationError):
            TaskUpdate(title="Test Task", description="Test Description", priority="invalid")

    def test_update_task_with_invalid_tags(self):
        with pytest.raises(ValidationError):
            TaskUpdate(title="Test Task", description="Test Description", tags= 2234)

    def test_update_task_with_invalid_created_at_in_the_future(self):
        with pytest.raises(ValidationError):
            TaskUpdate(title="Test Task", description="Test Description", created_at=date.today() + timedelta(days=1))

    def test_update_task_with_invalid_created_at_not_a_date(self):
        with pytest.raises(ValidationError):
            TaskUpdate(title="Test Task", description="Test Description", created_at="invalid")

class Test_task_get :
    def test_get_tasks(self):
        task = TaskCreate(title="Test Task", description="Test Description")
        assert task.title == "Test Task"
        assert task.description == "Test Description"


    def test_list_seeded_tasks(self, client_with_tasks):
        response = client_with_tasks.get("/tasks")
        assert len(response.json()) == 6

    def test_get_task_by_id(self, client_with_tasks):
        response = client_with_tasks.get("/tasks/1")
        assert response.json()["title"] == main.tasks[1].title
        assert response.json()["description"] == main.tasks[1].description
        assert response.json()["status"] == main.tasks[1].status
        assert response.json()["priority"] == main.tasks[1].priority
        assert response.json()["tags"] == main.tasks[1].tags
        assert response.json()["created_at"] == main.tasks[1].created_at.isoformat()

    def test_get_task_by_id_returns_404_when_task_not_found(self, client_with_tasks):
        response = client_with_tasks.get("/tasks/100")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_get_task_by_id_invalid_id(self, client_with_tasks):
        response = client_with_tasks.get("/tasks/invalid")
        assert response.status_code == 422

class Test_Task_post :
    def test_create_task(self, client_with_tasks):
        response = client_with_tasks.post("/tasks", json={"title": "Test Task", "description": "Test Description"})
        assert response.status_code == 201
        assert response.json()["title"] == "Test Task"
        assert response.json()["description"] == "Test Description"
        assert response.json()["status"] == "todo"
        assert response.json()["priority"] == "low"
        assert response.json()["tags"] == []
        assert response.json()["created_at"] == date.today().isoformat()

    def test_create_task_returns_error_with_empty_title(self, client_with_tasks):
        response = client_with_tasks.post("/tasks", json={"title": "", "description": "Test Description"})
        assert response.status_code == 422

    def test_create_task_returns_error_with_invalid_title(self, client_with_tasks):
        response = client_with_tasks.post("/tasks", json={"title": "A" * 51, "description": "Test Description"})
        assert response.status_code == 422

    def test_create_task_returns_error_with_invalid_description(self, client_with_tasks):
        response = client_with_tasks.post("/tasks", json={"title": "Test Task", "description": "A" * 201})
        assert response.status_code == 422

    def test_create_task_returns_error_with_invalid_status(self, client_with_tasks):
        response = client_with_tasks.post("/tasks", json={"title": "Test Task", "description": "Test Description", "status": "invalid"})
        assert response.status_code == 422

    def test_server_picks_increases_id_when_creating_task(self, client):
        first = client.post("/tasks", json={"title": "Test Task", "description": "Test Description"})
        assert first.status_code == 201
        assert first.json()["id"] == 1
        second = client.post("/tasks", json={"title": "Test Task 2", "description": "Test Description 2"})
        assert second.status_code == 201
        assert second.json()["id"] == 2

    def test_invalid_body_returns_422(self, client):
        response = client.post("/tasks", json="invalid")
        assert response.status_code == 422
        assert main.tasks == {}

    class Test_task_put :
        def test_update_task(self, client_with_tasks):
            response = client_with_tasks.put("/tasks/1", json={"title": "Updated Task", "description": "Updated Description", "status": "todo", "priority": "low", "tags": ["testUpdate"], "created_at": (date.today()- timedelta(days=4)).isoformat()})
            assert response.status_code == 200
            assert response.json()["title"] == "Updated Task"
            assert response.json()["description"] == "Updated Description"
            assert response.json()["status"] == "todo"
            assert response.json()["priority"] == "low"
            assert response.json()["tags"] == ["testUpdate"]
            assert response.json()["created_at"] == (date.today()- timedelta(days=4)).isoformat()

        def test_update_task_returns_error_with_empty_title(self, client_with_tasks):
            response = client_with_tasks.put("/tasks/1", json={"title": "", "description": "Test Description"})
            assert response.status_code == 422

        def test_uknown_id_returns_404(self, client_with_tasks):
            response = client_with_tasks.put("/tasks/100", json={"title": "Updated Task", "description": "Updated Description", "status": "todo", "priority": "low", "tags": ["testUpdate"], "created_at": (date.today()- timedelta(days=4)).isoformat()})
            assert response.status_code == 404
            assert response.json()["detail"] == "Task not found"

        def test_invalid_id_returns_422(self, client_with_tasks):
            response = client_with_tasks.put("/tasks/invalid", json={"title": "Updated Task", "description": "Updated Description", "status": "todo", "priority": "low", "tags": ["testUpdate"], "created_at": (date.today()- timedelta(days=4)).isoformat()})
            assert response.status_code == 422

        def test_invalid_body_returns_422(self, client_with_tasks):
            response = client_with_tasks.put("/tasks/1", json="invalid")
            assert response.status_code == 422


    class Test_task_delete :
        def test_delete_task_returns200_and_deletes_task(self, client_with_tasks):
            task_title = main.tasks[1].title
            response = client_with_tasks.delete("/tasks/1")
            assert response.status_code == 200
            assert response.json()["message"] == "Task deleted successfully"
            assert response.json()["task"] == task_title

        def test_delete_task_returns_404_when_task_not_found(self, client_with_tasks):
            response = client_with_tasks.delete("/tasks/100")
            assert response.status_code == 404
            assert response.json()["detail"] == "Task not found"

        def test_deleted_task_is_gone_from_the_list(self, client_with_tasks):
            task_title = main.tasks[4].title
            response = client_with_tasks.delete("/tasks/4")
            assert response.status_code == 200
            assert response.json()["message"] == "Task deleted successfully"
            assert response.json()["task"] == task_title
            assert list(main.tasks) == [1, 2, 3, 5, 6]

        def test_delete_task_by_title_returns200_and_deletes_task(self, client_with_tasks):
            task_title = main.tasks[4].title
            response = client_with_tasks.delete(f"/tasks/title/{task_title}")
            assert response.status_code == 200
            assert response.json()["message"] == "Task deleted successfully"
            assert response.json()["task"] == task_title
            assert list(main.tasks) == [1, 2, 3, 5, 6]

        def test_delete_task_by_title_returns_404_when_task_not_found(self, client_with_tasks):
            response = client_with_tasks.delete("/tasks/title/Invalid Task")
            assert response.status_code == 404
            assert response.json()["detail"] == "Task not found"

        def test_delete_task_by_title_Not_case_sensitive(self, client_with_tasks):
            response = client_with_tasks.delete("/tasks/title/buy laptop")
            assert response.status_code == 200
            assert response.json()["message"] == "Task deleted successfully"
            assert response.json()["task"] == "Buy Laptop"
            assert list(main.tasks) == [1, 2, 3, 5, 6]