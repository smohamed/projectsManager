from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from models.project import ProjectResponse
from models.user import UserRequest, UserResponse
from services.db import Db

api = APIRouter(prefix='/users',
                responses={
                    404: {"description": "Not a valid company"}
                },
                tags=['User'])

db = Db()


@api.get('/{user_id}/projects', response_model=list[ProjectResponse])
async def get_projects(user_id: int):
    return db.get_projects_by_user(user_id)


@api.post('/', response_model=UserResponse, status_code=HTTPStatus.CREATED)
async def create_user(user: UserRequest):
    user = db.create_user(user)
    if user:
        return user
    else:
        raise HTTPException(status_code=400, detail="Not a valid company")
