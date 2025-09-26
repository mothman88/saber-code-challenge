from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.crud.task import (
    create_task, get_tasks, get_task, update_task, delete_task
)
from app.database import get_db

router = APIRouter()

@router.post(
    "/tasks/",
    response_model=TaskOut,
    summary="Create a new task",
    description="Create a new task with the provided details including title, description, priority, and completion status."
)
def create_task_view(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.

    This endpoint allows creating a new task with the provided details.

    **Parameters:**
    - **task**: TaskCreate schema containing:
        - title (str): The task title (required)
        - description (str): Optional detailed description
        - priority (int): Priority level (optional, defaults to 1)
        - completed (bool): Completion status (optional, defaults to False)

    **Returns:**
    - TaskOut: The created task with all fields populated including ID and timestamps

    **Raises:**
    - HTTPException: If there's a validation error or database constraint violation (422)
    """
    return create_task(db, task)

@router.get(
    "/tasks/",
    response_model=List[TaskOut],
    summary="Retrieve tasks with filtering and pagination",
    description="Get a list of tasks with optional filtering by completion status and priority, text search, and pagination controls."
)
def read_tasks(
    completed: Optional[bool] = None,
    priority: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Retrieve tasks with optional filtering, searching, and pagination.

    This endpoint returns a list of tasks that can be filtered by various criteria
    and supports pagination for large result sets.

    **Query Parameters:**
    - **completed** (bool, optional): Filter by completion status
        - `true`: Only completed tasks
        - `false`: Only incomplete tasks
        - `null` (default): All tasks
    - **priority** (int, optional): Filter by priority level
    - **search** (str, optional): Search in task titles and descriptions (case-insensitive)
    - **skip** (int, default=0): Number of tasks to skip (for pagination)
    - **limit** (int, default=10): Maximum number of tasks to return (max 100)

    **Returns:**
    - List[TaskOut]: Array of task objects matching the filter criteria

    **Example:**
    ```
    GET /tasks/?completed=false&priority=1&search=urgent&limit=5
    ```
    """
    return get_tasks(db, completed, priority, search, skip, limit)

@router.get(
    "/tasks/{task_id}/",
    response_model=TaskOut,
    summary="Retrieve a specific task by ID",
    description="Get detailed information about a single task identified by its unique ID.",
    responses={
        200: {"description": "Task found and returned successfully"},
        404: {"description": "Task not found"}
    }
)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific task by its ID.

    This endpoint returns the complete details of a single task.

    **Path Parameters:**
    - **task_id** (int): The unique identifier of the task to retrieve

    **Returns:**
    - TaskOut: Complete task object with all fields

    **Raises:**
    - HTTPException (404): If the task with the specified ID does not exist

    **Example:**
    ```
    GET /tasks/123/
    ```
    """
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put(
    "/tasks/{task_id}/",
    response_model=TaskOut,
    summary="Update an existing task",
    description="Update the details of an existing task. Only provided fields will be updated.",
    responses={
        200: {"description": "Task updated successfully"},
        404: {"description": "Task not found"},
        422: {"description": "Validation error in request data"}
    }
)
def update_task_view(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update an existing task.

    This endpoint allows partial or full updates to an existing task. Only the fields
    provided in the request body will be updated.

    **Path Parameters:**
    - **task_id** (int): The unique identifier of the task to update

    **Request Body:**
    - **task**: TaskUpdate schema containing optional fields:
        - title (str, optional): Updated task title
        - description (str, optional): Updated description
        - priority (int, optional): Updated priority level
        - completed (bool, optional): Updated completion status

    **Returns:**
    - TaskOut: The updated task object with all current fields

    **Raises:**
    - HTTPException (404): If the task with the specified ID does not exist
    - HTTPException (422): If the request data fails validation

    **Example:**
    ```
    PUT /tasks/123/
    {
        "title": "Updated task title",
        "completed": true
    }
    ```
    """
    updated = update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated

@router.delete(
    "/tasks/{task_id}/",
    summary="Delete a task",
    description="Permanently delete a task by its ID. This action cannot be undone.",
    responses={
        200: {"description": "Task deleted successfully"},
        404: {"description": "Task not found"}
    }
)
def delete_task_view(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by its ID.

    This endpoint permanently removes a task from the database. This action cannot be undone.

    **Path Parameters:**
    - **task_id** (int): The unique identifier of the task to delete

    **Returns:**
    - dict: Confirmation message with format `{"message": "Task deleted successfully"}`

    **Raises:**
    - HTTPException (404): If the task with the specified ID does not exist

    **Example:**
    ```
    DELETE /tasks/123/
    Response: {"message": "Task deleted successfully"}
    ```
    """
    deleted = delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
