import pytest
import requests

# Define the URL endpoint for the API (replace with your actual API endpoint)
BASE_URL = "http://example.com/api/tasks"

# Sample data-driven test using pytest parameterization
@pytest.mark.parametrize("task_name, description, expected_status_code", [
    ("Sample Task", "This is a normal task", 201),                # Normal input
    ("", "Task without a name", 400),                             # Empty task name
    ("SpecialChar@#$%", "Task with special characters", 201),     # Special characters in task name
    ("Long" * 100, "Task with a very long name", 400),            # Exceeding max length
    ("Valid Name", "", 201),                                      # Empty description
    (None, "Task with None as name", 400)                         # None as task name
])
def test_create_task(task_name, description, expected_status_code):
    # Data payload for the API request
    payload = {
        "task_name": task_name,
        "description": description
    }

    # Send POST request to create a task
    response = requests.post(f"{BASE_URL}/create", json=payload)
    
    # Assert the response status code matches the expected status code
    assert response.status_code == expected_status_code

    # Additional checks can be done here, such as validating response body
    # For example: assert response.json().get("task_name") == task_name