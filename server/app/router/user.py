# Imports
from typing import Annotated, Type, Optional, Any, Tuple
from copy import deepcopy
from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from ..database.models import Users
from ..database.database import SessionLocal

# Set Up Router
router = APIRouter(
    prefix='/user',
    tags=['users']
)

# Set up database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Set up database dependency
db_dependency = Annotated[Session, Depends(get_db)]

# User Request Structure Classes
class UserBodyRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    email: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=3, max_length=20)
    is_active: bool
    role: str

def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new_field = deepcopy(field)
        new_field.default = default
        new_field.annotation = Optional[field.annotation]
        return new_field.annotation, new_field
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        }
    )

@partial_model
class UserUpdateRequest(UserBodyRequest):
    pass

# Helper Methods
def to_keys(request: UserUpdateRequest):
    return [key for key in dir(request) if not key.startswith('__')]

# API Methods
'''
CREATE METHOD:
Creates a user
'''
@router.post('/', status_code=status.HTTP_200_OK)
async def create_user(user_body: UserBodyRequest, db: db_dependency):
    user_model = Users(**user_body.model_dump())
    db.add(user_model)
    db.commit()

'''
READ METHOD:
Gets all users
'''
@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    return db.query(Users).all()

'''
READ METHOD:
Gets a user by id
'''
@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency, user_id: int = Path(gt=0)):
    return db.query(Users).filter(Users.id == user_id).first()

'''
UPDATE METHOD:
Updates a user by id
'''
@router.put('/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_update: UserUpdateRequest, db: db_dependency, user_id: int = Path(gt=0)):
    user_model = db.query(Users).filter(Users.id == user_id).first()
    keys = to_keys(user_update)
    if "username" in keys:
        user_model.username = user_update.username
    if "email" in keys:
        user_model.email = user_update.email
    if "password" in keys:
        user_model.password = user_update.password
    if "is_active" in keys:
        user_model.is_active = user_update.is_active
    if "role" in keys:
        user_model.role = user_update.role
    db.add(user_model)
    db.commit()

'''
DELETE METHOD:
Deletes a user by id
'''
@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(db: db_dependency, user_id: int = Path(gt=0)):
    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
    