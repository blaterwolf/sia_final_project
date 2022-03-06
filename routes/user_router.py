from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from schemas.user_schema import CreateUser
from models.user_model import User
from database import get_db
from dependencies import get_token


router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(get_token)]
)


@router.get('/')
def all(db: Session = Depends(get_db), current_user: User = Depends(get_token)):
    """Gets all users in the database.

    Args:
        db: Session object where cinacall niya yung database.

    Returns:
        (dict): All Users in the database.
    """
    print(current_user)
    users = db.query(User).all()
    # # returns list of all users [{...}, {...}, {...}] <- list comprehension?
    return {'users': [
        {
            'user_id': user.user_id,
            'user_name': user.user_name,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
        for user in users
    ]
    }


@router.get('/current')
def find_by_id(current_user: User = Depends(get_token), db: Session = Depends(get_db)):
    """Gets user information of the currently logged in user.

    Args:
        id (str): UUID based ID from the database
        db: Session object where cinacall niya yung database.

    Raises:
        HTTPException: 404 -> wala pong ganyang user.

    Returns:
        (dict): yung user na may similar ID na yun.
    """
    user = db.query(User).filter(
        User.user_id == current_user['author_id']).first()
    if not user:
        raise HTTPException(404, 'User not found')
    return {
        'user': {
            'user_id': user.user_id,
            'user_name': user.user_name,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        }
    }


@router.put('/update')
def update(user: CreateUser, db: Session = Depends(get_db), current_user: User = Depends(get_token)):
    """Updates the user information in the database of the currently logged in user.

    Args:
        id (str): The User ID.
        user (CreateUser): The CreateUser Schema is the provided data from the user.
        db: Session object where cinacall niya yung database.

    Raises:
        HTTPException: 404 -> wala pong ganyang user.

    Returns:
        json['message']: User updated successfully.
    """
    if not db.query(User).filter(User.user_id == current_user['author_id']).update({
        'user_name': user.user_name,
        'password': user.password
    }):
        raise HTTPException(404, 'User not found. Failed to update.')
    db.commit()
    return {'message': 'User updated successfully.'}


@router.delete('/{id}')
def remove(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_token)):
    """Deletes the user from the database by the provided id. Current user cannot delete itself. (duh)

    Args:
        id (str): The User ID.
        db: Session object where cinacall niya yung database.

    Raises:
        HTTPException: 404 -> wala pong ganyang user.

    Returns:
        json['message']: User deleted successfully.
    """
    if not db.query(User).filter(User.user_id == id, current_user['author_id'] != User.user_id).delete():
        raise HTTPException(
            404, 'User not found or you are deleting yourself. Deletion failed.')
    db.commit()
    return {'message': 'User removed successfully.'}
