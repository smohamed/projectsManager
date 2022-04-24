from typing import Tuple

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.db_models.db_base_model import DbBaseModel


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
