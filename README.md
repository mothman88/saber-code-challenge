# Task Manager API

A RESTful API to manage a simple task management system where users can create,
update, and delete tasks. 

## Build Commands

### Install Dependencies

Using uv (recommended):
```sh
uv sync
```

Or using pip:
```sh
pip install -r requirements.txt
```

### Run Locally

```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000

# for developement you can use the --reload flag
uvicorn app.main:app --reload
```

### API Documentation

Once the server is running, the API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Run Tests

```sh
uv run pytest
```

### Build Docker Image

```sh
docker build -t task-api .
```

to test the docker build locally:
```sh
docker run -it -p 8000:8000 task-api
```
