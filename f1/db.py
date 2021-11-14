"""

"""
import logging
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from f1 import settings  # noqa

DeclarativeBase = declarative_base()

logger = logging.getLogger(__name__)


def db_connect(
    db_conn_str: Optional[str] = None, debug: bool = False, timeout: int = 300
) -> Engine:
    """
    Performs database connection using database settings from settings.py.

    Returns sqlalchemy engine instance
    """
    db_connection = db_conn_str or settings.db_url

    connect_args = {}

    if not db_connection:
        raise Exception("Require db connection URL")

    if db_connection.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    try:
        return create_engine(
            db_connection,
            echo=debug,
            connect_args=connect_args,
        )
    except Exception as exc:
        logger.error("Could not connect to database: %s", exc)
        raise exc


engine = db_connect()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

SessionAutocommit = sessionmaker(bind=engine, autocommit=True, autoflush=True)
