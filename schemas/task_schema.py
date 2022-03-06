from datetime import datetime as dt
from pydantic import BaseModel


class TaskBase(BaseModel):
    task_name: str

# * Schema for request body
# ? Kapag nagrequest si user ng task, ito yung gagamitin na class name para descriptive, since same rin naman siya ng properties


class CreateTask(TaskBase):
    pass


class UpdateTask(TaskBase):
    task_id: str
    task_is_complete: bool


class Task(TaskBase):
    created_at: dt
    updated_at: dt
