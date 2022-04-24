from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from models.company import CompanyRequest, CompanyResponse
from models.project import ProjectDetailsResponse, ProjectRequest, ProjectResponse
from models.user import UserRequest, UserResponse
from services.db import Db

app = FastAPI(debug=True, port=5001)


db = Db()


@app.get('/projects', response_model=list[ProjectResponse])
async def get_projects():
    return db.get_all_projects()


@app.get('/projects/{project_id}', response_model=ProjectDetailsResponse)
async def get_project(project_id: int):
    project = db.get_project(project_id)
    if project:
        return project
    else:
        raise HTTPException(status_code=404, detail="Project not found")


@app.get('/companies/{company_id}/projects', response_model=list[ProjectResponse])
async def get_projects(company_id: int):
    return db.get_projects_by_company(company_id)


@app.get('/companies/{company_id}/users/{user_id}/projects', response_model=list[ProjectResponse])
async def get_projects(company_id: int, user_id: int):
    return db.get_projects_by_company_and_user(company_id, user_id)


@app.get('/users/{user_id}/projects', response_model=list[ProjectResponse])
async def get_projects(user_id: int):
    return db.get_projects_by_user(user_id)


@app.post('/companies', response_model=CompanyResponse, status_code=HTTPStatus.CREATED)
async def create_company(company: CompanyRequest):
    return db.create_company(company)


@app.post('/users', response_model=UserResponse, status_code=HTTPStatus.CREATED)
async def create_user(user: UserRequest):
    user = db.create_user(user)
    if user:
        return user
    else:
        raise HTTPException(status_code=400, detail="Not a valid company")


@app.post('/projects', response_model=ProjectResponse, status_code=HTTPStatus.CREATED)
async def create_project(project: ProjectRequest):
    project = db.create_project(project)
    if project:
        return project
    else:
        raise HTTPException(status_code=400, detail="Company or user is not valid")
