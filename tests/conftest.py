import app.main as main
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """ A Test Client with no database talking tot he API."""
    main.tasks.clear()
    yield TestClient(main.app)
    main.tasks.clear()


@pytest.fixture
def client_with_tasks():
    """A test client loaded with the original seeded tasks."""
    main.seed_tasks()
    yield TestClient(main.app)
    main.tasks.clear()