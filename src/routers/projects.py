from http import HTTPStatus

from api_models.project import (ProjectDetailsResponse, ProjectRequest,
                                ProjectResponse, ProjectStatus)
from fastapi import APIRouter
from services.db import get_exception
from services.db_models.project import Project
from services.repository.project import ProjectRepo

error_invalid_project = {
    404: {'description': 'Project not found'}}
error_invalid_company = {
    400: {'description': 'Not a valid company'}}
error_invalid_user = {
    400: {'description': 'Not a valid user'}}
error_project_name__unique = {
    409: {'description': 'Project name must be unique'}}
error_invalid_project_status = {
    409: {'description': 'Project status is not valid'}}

api = APIRouter(prefix='/projects', tags=['Project'])
db = ProjectRepo()


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


def update_project_status(project_id: int, new_status: ProjectStatus,
                          orignal_status: ProjectStatus):
    project = db.update_project_status(project_id, new_status, orignal_status)
    if project is None or project == 1:
        raise get_exception(list(error_invalid_project.items())[0])
    elif isinstance(project, Project):
        return project
    else:
        raise get_exception(list(error_invalid_project_status.items())[0])


@api.post('/start/{project_id}', status_code=HTTPStatus.NO_CONTENT,
          responses={**error_invalid_project, **error_invalid_project_status})
async def start_project(project_id: int):
    return update_project_status(project_id, ProjectStatus.IN_PROGRESS, ProjectStatus.TO_DO)


@api.post('/finish/{project_id}', status_code=HTTPStatus.NO_CONTENT,
          responses={**error_invalid_project, **error_invalid_project_status})
async def finish_project(project_id: int):
    return update_project_status(project_id, ProjectStatus.FINISHED, ProjectStatus.IN_PROGRESS)


@api.post('/close/{project_id}', status_code=HTTPStatus.NO_CONTENT,
          responses={**error_invalid_project, **error_invalid_project_status})
async def close_project(project_id: int):
    return update_project_status(project_id, ProjectStatus.CLOSED, ProjectStatus.FINISHED)
