from api_models.project import (ProjectDetailsResponse, ProjectRequest,
                                ProjectResponse, ProjectStatus)
from services.db import Db
from services.db_models.company import Company
from services.db_models.project import Project
from services.db_models.user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class ProjectRepo(Db):
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
            project = db.get(Project, project_id)
            return project
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

    def update_project_status(self, project_id: int, status: ProjectStatus,
                              orignal_status: ProjectStatus) -> ProjectResponse:
        db: Session = self.DatabaseRef()
        try:
            project = db.get(Project, project_id)
            if not project:
                return 1

            if project.status != orignal_status:
                return 2

            project.status = status
            db.add(project)
            db.commit()
            return project
        finally:
            db.close()
