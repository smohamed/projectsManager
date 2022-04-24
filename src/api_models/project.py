from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ProjectStatus(Enum):
    TO_DO = 'to do'
    IN_PROGRESS = 'in progress'
    FINISHED = 'finished'
    CLOSED = 'closed'


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
    status: ProjectStatus
    created: datetime
    updated: Optional[datetime] = None

    class Config:
        orm_mode = True
