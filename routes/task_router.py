from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.task_schema import CreateTask, UpdateTask, TaskBase
from models.user_model import User
from models.task_model import Task
from database import get_db
from dependencies import get_token
from jose import JWTError

router = APIRouter(
    prefix='/tasks',
    tags=['tasks'],
    dependencies=[Depends(get_token)]
)


@router.get('/')
def all_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_token)):
    """Gets all tasks in the database of the currently logged in user.

    Args:
        db: Session object where cinacall niya yung database.
        current_user: User object of the currently logged in user.

    Returns:
        (dict): All Tasks in the database by the current user logged in.
    """
    tasks = db.query(Task).filter(
        current_user['author_id'] == Task.author_id).all()
    return {'tasks': [each_task.task_name for each_task in tasks]}


@router.get('/done')
def done_task(db: Session = Depends(get_db), current_user: User = Depends(get_token)):
    """Gets all tasks that is marked as done in the database of the currently logged in user.

    Args:
        db: Session object where cinacall niya yung database.

    Returns:
        (dict): All Tasks in the database that is marked as done by the current user logged in.
    """
    tasks = db.query(Task).filter(
        current_user['author_id'] == Task.author_id, Task.task_is_complete == 1).all()
    return {'tasks': [each_task.task_name for each_task in tasks]}


@router.post('/')
def create(task: CreateTask, db: Session = Depends(get_db), current_user: User = Depends(get_token)):
    """Creates a new task in the database.

    Args:
        task: Task object to be created
        db: Session object where cinacall niya yung database.

    Returns:
        (str): Task created successfully.
    """
    try:
        author_id = current_user['author_id']
        new_task = Task(
            author_id=author_id,
            task_name=task.task_name
        )
        db.add(new_task)
        db.commit()
        return {'message': 'Task created successfully!'}
    except JWTError:
        raise HTTPException(status_code=400, detail='Invalid JWT token')


@router.put('/')
def update_task(taskReq: UpdateTask, db: Session = Depends(get_db), current_user: User = Depends(get_token)):
    """Update tasks in the database based on the task_id provided by the user.

    Args:
        task_id (str): This is the TaskID provided by the user in the link.
        taskReq (UpdateTask): The UpdateTask Schema is the provided data from the user.
        db: Session object where cinacall niya yung database.

    Raises:
        HTTPException: 404 -> wala pong ganyang task.

    Returns:
        json['message']: Task updated successfully.
    """
    if not db.query(Task).filter(Task.task_id == taskReq.task_id, current_user['author_id'] == Task.author_id).update({
        'task_name': taskReq.task_name,
        'task_is_complete': taskReq.task_is_complete
    }):
        raise HTTPException(404, 'Task not found. Failed to update.')
    db.commit()
    return {
        'message': 'Task updated successfully!',
    }


@router.delete('/')
def delete_task(taskReq: TaskBase, db: Session = Depends(get_db), current_user: User = Depends(get_token)):
    """Deletes the task by the task_id provided by the user.

    Args:
        task_id (str): _description_
        db: Session object where cinacall niya yung database.

    Raises:
        HTTPException: 404 -> wala pong ganyang task.

    Returns:
        json['message']: Task deleted successfully.
        json['task_deleted']: Details of the task you deleted.
    """
    if not db.query(Task).filter(Task.task_name == taskReq.task_name,
                                 current_user['author_id'] == Task.author_id).delete():
        raise HTTPException(404, 'Task not found. Deletion failed.')
    db.commit()
    return {'message': 'Task deleted successfully!', }
