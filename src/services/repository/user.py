from models.project import ProjectResponse
from models.user import UserRequest, UserResponse
from services.db import Db
from services.models.company import Company
from services.models.project import Project
from services.models.user import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class UserRepo(Db):
    def get_projects(self, user_id: int) -> list[ProjectResponse]:
        db: Session = self.DatabaseRef()
        try:
            projects = db.query(Project).filter(
                Project.user_id == user_id).all()
            return projects
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
