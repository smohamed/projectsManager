from models.project import (ProjectDetailsResponse, ProjectRequest,
                            ProjectResponse, ProjectStatus)
from services.db import Db
from services.models.company import Company
from services.models.project import Project
from services.models.user import User
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
            project = db.query(Project).filter(
                Project.id == project_id).first()
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