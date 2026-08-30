"""A small task API used in lesson 14."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Annotated, Protocol

from fastapi import Depends, FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    priority: int = Field(default=3, ge=1, le=5)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("title must not be blank")
        return normalized


class TaskPublic(BaseModel):
    id: int
    title: str
    priority: int
    done: bool


class TaskRepository(Protocol):
    def add(self, data: TaskCreate) -> TaskPublic: ...

    def all(self) -> list[TaskPublic]: ...

    def mark_done(self, task_id: int) -> TaskPublic | None: ...


class MemoryTaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[int, TaskPublic] = {}
        self._next_id = 1

    def add(self, data: TaskCreate) -> TaskPublic:
        task = TaskPublic(
            id=self._next_id,
            title=data.title,
            priority=data.priority,
            done=False,
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def all(self) -> list[TaskPublic]:
        return sorted(self._tasks.values(), key=lambda task: (-task.priority, task.id))

    def mark_done(self, task_id: int) -> TaskPublic | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        updated = task.model_copy(update={"done": True})
        self._tasks[task_id] = updated
        return updated


def get_repository(request: Request) -> TaskRepository:
    return request.app.state.repository


RepositoryDep = Annotated[TaskRepository, Depends(get_repository)]


def create_app(repository: TaskRepository | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.repository = (
            repository if repository is not None else MemoryTaskRepository()
        )
        yield

    app = FastAPI(
        title=os.getenv("APP_NAME", "Course Task API"),
        lifespan=lifespan,
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post(
        "/tasks",
        response_model=TaskPublic,
        status_code=status.HTTP_201_CREATED,
    )
    def create_task(data: TaskCreate, tasks: RepositoryDep) -> TaskPublic:
        return tasks.add(data)

    @app.get("/tasks", response_model=list[TaskPublic])
    def list_tasks(tasks: RepositoryDep) -> list[TaskPublic]:
        return tasks.all()

    @app.post("/tasks/{task_id}/done", response_model=TaskPublic)
    def mark_task_done(task_id: int, tasks: RepositoryDep) -> TaskPublic:
        task = tasks.mark_done(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    return app


app = create_app()
