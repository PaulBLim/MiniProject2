from main import TaskCreate
from pydantic import ValidationError
import pytest
from datetime import date
class test_task_create :
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

class test_default_values :
    def test_default_values(self):
        task = TaskCreate(title="Test Task")
        assert task.description == ""
        assert task.status == "todo"
        assert task.priority == "low"
        assert task.tags == []
        assert task.created_at == date.today()