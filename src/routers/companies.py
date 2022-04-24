from http import HTTPStatus

from fastapi import APIRouter
from models.company import CompanyRequest, CompanyResponse
from models.project import ProjectResponse
from services.db import Db

api = APIRouter(prefix='/companies')
db = Db()


@api.get('/{company_id}/projects', response_model=list[ProjectResponse])
async def get_projects(company_id: int):
    return db.get_projects_by_company(company_id)


@api.get('/{company_id}/users/{user_id}/projects', response_model=list[ProjectResponse])
async def get_projects(company_id: int, user_id: int):
    return db.get_projects_by_company_and_user(company_id, user_id)


@api.post('/', response_model=CompanyResponse, status_code=HTTPStatus.CREATED)
async def create_company(company: CompanyRequest):
    return db.create_company(company)
