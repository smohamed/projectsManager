from http import HTTPStatus

from fastapi import APIRouter
from models.project import ProjectResponse
from models.user import UserRequest, UserResponse
from services.db import Db, get_exception
from services.models.user import User

error_invalid_company = {
    400: {'description': 'Not a valid company'}}
error_user_name__unique = {
    409: {'description': 'User name must be unique'}}

api = APIRouter(prefix='/users', tags=['User'])
db = Db()


@api.get('/{user_id}/projects', response_model=list[ProjectResponse])
async def get_projects(user_id: int):
    return db.get_projects_by_user(user_id)


@api.post('/', response_model=UserResponse, status_code=HTTPStatus.CREATED,
          responses={**error_invalid_company, **error_user_name__unique})
async def create_user(user: UserRequest):
    user = db.create_user(user)
    if user and isinstance(user, User):
        return user
    elif user == 1:
        raise get_exception(list(error_invalid_company.items())[0])
    else:
        raise get_exception(list(error_user_name__unique.items())[0])
