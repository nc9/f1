"""

"""
from typing import Optional

from pydantic import BaseSettings
from pydantic.networks import AnyUrl


class AppSettings(BaseSettings):
    env: str = "development"

    log_level: str = "DEBUG"

    db_url: Optional[AnyUrl]

    class Config:
        fields = {
            "db_url": {"env": "DATABASE_HOST_URL"},
        }
