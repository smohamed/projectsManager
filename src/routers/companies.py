from http import HTTPStatus

from api_models.company import CompanyRequest, CompanyResponse
from api_models.project import ProjectResponse
from fastapi import APIRouter
from services.db import get_exception
from services.db_models.company import Company
from services.repository.company import CompnayRepo

error_company_name__unique = {
    409: {'description': 'Company name must be unique'}}

api = APIRouter(prefix='/companies', tags=['Company'])
db = CompnayRepo()


@api.get('/{company_id}/projects', response_model=list[ProjectResponse])
async def get_projects(company_id: int):
    return db.get_projects(company_id)


@api.get('/{company_id}/users/{user_id}/projects', response_model=list[ProjectResponse])
async def get_projects(company_id: int, user_id: int):
    return db.get_projects_for_user(company_id, user_id)


@api.post('/', response_model=CompanyResponse, status_code=HTTPStatus.CREATED,
          responses={**error_company_name__unique})
async def create_company(company: CompanyRequest):
    company = db.create_company(company)
    if company and isinstance(company, Company):
        return company
    else:
        raise get_exception(list(error_company_name__unique.items())[0])
