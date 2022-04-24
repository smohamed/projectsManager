from ..models.db_base_model import DbBaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Company(DbBaseModel):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="company")
    projects = relationship("Project", back_populates="company")
