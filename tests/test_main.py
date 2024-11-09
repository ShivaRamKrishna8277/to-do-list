# test_main.py
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

# Create a TestClient for our FastAPI app
client = TestClient(app)

# Sample test data
sample_task = {
    "title": "Sample Task",
    "description": "This is a sample to-do item."
}

# Test adding a new task
def test_create_task():
    response = client.post("/todos", json=sample_task)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_task["title"]
    assert data["description"] == sample_task["description"]
    assert "id" in data  # Check if the task has an ID

# Test retrieving all tasks
def test_get_tasks():
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Check if the response is a list
    assert any(task["title"] == sample_task["title"] for task in data)  # Check if the sample task exists

# Test updating a task
def test_update_task():
    # First, add a task to ensure it exists
    create_response = client.post("/todos", json=sample_task)
    task_id = create_response.json()["id"]
    
    updated_task = {
        "title": "Updated Task",
        "description": "This is an updated task description."
    }

    # Update the task
    update_response = client.put(f"/todos/{task_id}", json=updated_task)
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == updated_task["title"]
    assert data["description"] == updated_task["description"]

# Test deleting a task
def test_delete_task():
    # First, add a task to ensure it exists
    create_response = client.post("/todos", json=sample_task)
    task_id = create_response.json()["id"]

    # Delete the task
    delete_response = client.delete(f"/todos/{task_id}")
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert data["message"] == "Task deleted successfully"  # Updated message
