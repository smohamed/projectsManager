
from models.company import CompanyRequest, CompanyResponse
from models.project import ProjectResponse
from services.db import Db
from services.models.company import Company
from services.models.project import Project
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class CompnayRepo(Db):
    def get_projects(self, company_id: int) -> list[ProjectResponse]:
        db: Session = self.DatabaseRef()
        try:
            projects = db.query(Project).filter(
                Project.company_id == company_id).all()
            return projects
        finally:
            db.close()

    def get_projects_for_user(self, company_id: int, user_id: int) -> list[ProjectResponse]:
        db: Session = self.DatabaseRef()
        try:
            projects = db.query(Project).filter(
                Project.company_id == company_id, Project.user_id == user_id).all()
            return projects
        finally:
            db.close()

    def create_company(self, company: CompanyRequest) -> CompanyResponse:
        db: Session = self.DatabaseRef()
        try:
            company = Company(**company.dict())
            db.add(company)
            db.commit()
            db.refresh(company)
            return company
        except IntegrityError:
            return 1
        finally:
            db.close()
