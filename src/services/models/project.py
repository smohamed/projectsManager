from datetime import datetime

from services.models.db_base_model import DbBaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Project(DbBaseModel):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    created = Column(DateTime, default=datetime.utcnow())
    updated = Column(DateTime, default=None)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="projects")
    creator = relationship("User", back_populates="projects")
