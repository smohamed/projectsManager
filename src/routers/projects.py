from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from models.project import (ProjectDetailsResponse, ProjectRequest,
                            ProjectResponse)
from services.db import Db

api = APIRouter(prefix='/projects',
                         responses={
                             400: {"description": "Company or user is not valid"},
                             404: {"description": "Project not found"}
                         })

db = Db()


@api.get('/', response_model=list[ProjectResponse])
async def get_projects():
    return db.get_all_projects()


@api.get('/{project_id}', response_model=ProjectDetailsResponse)
async def get_project(project_id: int):
    project = db.get_project(project_id)
    if project:
        return project
    else:
        raise HTTPException(status_code=404, detail="Project not found")


@api.post('/', response_model=ProjectResponse, status_code=HTTPStatus.CREATED)
async def create_project(project: ProjectRequest):
    project = db.create_project(project)
    if project:
        return project
    else:
        raise HTTPException(
            status_code=400, detail="Company or user is not valid")
