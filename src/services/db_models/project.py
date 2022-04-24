from datetime import datetime

from api_models.project import ProjectStatus
from services.db_models.db_base_model import DbBaseModel
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Project(DbBaseModel):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    status = Column(Enum(ProjectStatus))
    created = Column(DateTime, default=datetime.utcnow())
    updated = Column(DateTime, default=None)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="projects")
    creator = relationship("User", back_populates="projects")
