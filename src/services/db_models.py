from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DbBaseModel = declarative_base()


class Company(DbBaseModel):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="company")
    projects = relationship("Project", back_populates="company")


class User(DbBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="users")
    projects = relationship("Project", back_populates="creator")


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
