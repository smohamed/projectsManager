from typing import Tuple

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from models.company import CompanyRequest, CompanyResponse
from models.project import (ProjectDetailsResponse, ProjectRequest,
                            ProjectResponse, ProjectStatus)
from models.user import UserRequest, UserResponse
from services.models.company import Company
from services.models.db_base_model import DbBaseModel
from services.models.project import Project
from services.models.user import User


def get_exception(error: Tuple[int, dict[str, str]]) -> HTTPException:
    return HTTPException(status_code=error[0], detail=error[1]['description'])


class Db:
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./projects.db"

    def __init__(self) -> None:
        engine = create_engine(self.SQLALCHEMY_DATABASE_URL, connect_args={
                               "check_same_thread": False})

        self.DatabaseRef = sessionmaker(
            autocommit=False, autoflush=False, bind=engine)

        DbBaseModel.metadata.create_all(bind=engine)

    def get_all_projects(self) -> list[ProjectResponse]:
        db: Session = self.DatabaseRef()
        try:
            projects = db.query(Project).all()
            return projects
        finally:
            db.close()

    def get_project(self, project_id: int) -> ProjectDetailsResponse:
        db: Session = self.DatabaseRef()
        try:
            project = db.query(Project).filter(
                Project.id == project_id).first()
            return project
        finally:
            db.close()

    def get_projects_by_company(self, company_id: int) -> list[ProjectResponse]:
        db: Session = self.DatabaseRef()
        try:
            projects = db.query(Project).filter(
                Project.company_id == company_id).all()
            return projects
        finally:
            db.close()

    def get_projects_by_company_and_user(self, company_id: int, user_id: int) -> list[ProjectResponse]:
        db: Session = self.DatabaseRef()
        try:
            projects = db.query(Project).filter(
                Project.company_id == company_id, Project.user_id == user_id).all()
            return projects
        finally:
            db.close()

    def get_projects_by_user(self, user_id: int) -> list[ProjectResponse]:
        db: Session = self.DatabaseRef()
        try:
            projects = db.query(Project).filter(
                Project.user_id == user_id).all()
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

    def create_user(self, user: UserRequest) -> UserResponse:
        db: Session = self.DatabaseRef()
        try:
            company = db.query(Company).filter(
                Company.id == user.company_id).first()
            if not company:
                return 1

            user = User(**user.dict(), company=company)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            return 2
        finally:
            db.close()

    def create_project(self, project: ProjectRequest) -> ProjectResponse:
        db: Session = self.DatabaseRef()
        try:
            company = db.query(Company).filter(
                Company.id == project.company_id).first()
            if not company:
                return 1

            user = db.query(User).filter(
                User.id == project.user_id and User.company == project.company_id).first()
            if not user:
                return 2

            project = Project(
                **project.dict(), status=ProjectStatus.TO_DO, company=company, creator=user)
            db.add(project)
            db.commit()
            db.refresh(project)
            return project
        except IntegrityError:
            return 3
        finally:
            db.close()
