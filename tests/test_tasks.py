# Shared task creation for reuse
def create_sample_task(client):
    response = client.post("/tasks/", json={
        "title": "Sample Task",
        "description": "Test description",
        "priority": 1,
        "due_date": "2030-01-01T00:00:00"
    })
    return response.json()["id"]

# POST /tasks/
def test_create_task_success(client):
    response = client.post("/tasks/", json={
        "title": "New Task",
        "description": "Details",
        "priority": 2,
        "due_date": "2030-01-01T00:00:00"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "New Task"

def test_create_task_missing_title(client):
    response = client.post("/tasks/", json={
        "description": "Missing title",
        "priority": 1,
        "due_date": "2030-01-01T00:00:00"
    })
    assert response.status_code == 422

def test_create_task_invalid_priority(client):
    response = client.post("/tasks/", json={
        "title": "Bad Priority",
        "priority": 99,
        "due_date": "2030-01-01T00:00:00"
    })
    assert response.status_code == 422

# GET /tasks/
def test_get_all_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_tasks_with_filters(client):
    client.post("/tasks/", json={
        "title": "Filtered Task",
        "description": "Completed",
        "priority": 1,
        "due_date": "2030-01-01T00:00:00"
    })
    response = client.get("/tasks/?priority=1&completed=false")
    assert response.status_code == 200

# GET /tasks/{task_id}/
def test_get_task_by_id(client):
    task_id = create_sample_task(client)
    response = client.get(f"/tasks/{task_id}/")
    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_get_task_invalid_id(client):
    response = client.get("/tasks/invalid/")
    assert response.status_code == 422

def test_get_task_not_found(client):
    response = client.get("/tasks/999999/")
    assert response.status_code == 404

# PUT /tasks/{task_id}/
def test_update_task_success(client):
    task_id = create_sample_task(client)
    response = client.put(f"/tasks/{task_id}/", json={
        "title": "Updated Title",
        "completed": True
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["completed"] is True

def test_update_task_not_found(client):
    response = client.put("/tasks/999999/", json={"title": "Ghost"})
    assert response.status_code == 404

def test_update_task_invalid_data(client):
    task_id = create_sample_task(client)
    response = client.put(f"/tasks/{task_id}/", json={"priority": "high"})
    assert response.status_code == 422

# DELETE /tasks/{task_id}/
def test_delete_task_success(client):
    task_id = create_sample_task(client)
    response = client.delete(f"/tasks/{task_id}/")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

def test_delete_task_not_found(client):
    response = client.delete("/tasks/999999/")
    assert response.status_code == 404
