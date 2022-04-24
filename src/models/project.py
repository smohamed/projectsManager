from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str


class ProjectRequest(ProjectBase):
    description: str
    user_id: int
    company_id: int


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        orm_mode = True


class ProjectDetailsResponse(ProjectRequest):
    id: int
    created: datetime
    updated: Optional[datetime] = None

    class Config:
        orm_mode = True
