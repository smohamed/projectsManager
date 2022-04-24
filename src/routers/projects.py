from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from models.project import (ProjectDetailsResponse, ProjectRequest,
                            ProjectResponse)
from services.db import Db, get_exception
from services.models.project import Project

error_invalid_project = {
    404: {'description': 'Project not found'}}
error_invalid_company = {
    400: {'description': 'Not a valid company'}}
error_invalid_user = {
    400: {'description': 'Not a valid user'}}
error_project_name__unique = {
    409: {'description': 'Project name must be unique'}}

api = APIRouter(prefix='/projects', tags=['Project'])
db = Db()


@api.get('/', response_model=list[ProjectResponse])
async def get_projects():
    return db.get_all_projects()


@api.get('/{project_id}', response_model=ProjectDetailsResponse,
         responses={**error_invalid_project})
async def get_project(project_id: int):
    project = db.get_project(project_id)
    if project:
        return project
    else:
        raise get_exception(list(error_invalid_project.items())[0])


@api.post('/', response_model=ProjectResponse, status_code=HTTPStatus.CREATED,
          responses={**error_invalid_company, **error_invalid_user,
                     **error_project_name__unique})
async def create_project(project: ProjectRequest):
    project = db.create_project(project)
    if project and isinstance(project, Project):
        return project
    elif project == 1:
        raise get_exception(list(error_invalid_company.items())[0])
    elif project == 2:
        raise get_exception(list(error_invalid_user.items())[0])
    else:
        raise get_exception(list(error_project_name__unique.items())[0])
