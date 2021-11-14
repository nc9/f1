"""
Base models defined as both pydantic models and sqlalchemy models
"""

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.main import default_registry

Base = default_registry.generate_base()
metadata = Base.metadata  # type: ignore


class Circuits(SQLModel, table=True):
    id: int = Field(..., primary_key=True)
    code: str
    name: str
    location: str
    country: str
    altitude: int
    url: str


class Drivers(SQLModel, table=True):
    id: int = Field(..., primary_key=True)
    code: str
    number: Optional[int]
    acronym: Optional[str]
    name_first: str
    name_last: str
    dob: date
    nationality: str
    url: str


class Constructors(SQLModel, table=True):
    id: int = Field(..., primary_key=True)
    code: str
    name: str
    nationality: str
    url: str


class Races(SQLModel, table=True):
    id: int = Field(..., primary_key=True)
    year: int
    round: int
    circuit_id: int = Field(..., foreign_key="circuits.id")
    name: str
    start: datetime
    url: str


class ResultsStatus(SQLModel, table=True):
    id: int = Field(..., primary_key=True)
    status: str


class Results(SQLModel, table=True):
    id: int = Field(..., primary_key=True)
    race_id: int = Field(..., foreign_key="races.id")
    driver_id: int = Field(..., foreign_key="drivers.id")
    constructor_id: int = Field(..., foreign_key="constructors.id")
    status_id: int = Field(..., foreign_key="resultsstatus.id")
    number: Optional[int]
    grid: int
    position: Optional[int]
    position_status: str
    position_order: int
    points: float
    laps: int
    time: Optional[int]


class Laps(SQLModel, table=True):
    race_id: int = Field(..., foreign_key="races.id", primary_key=True)
    driver_id: int = Field(..., foreign_key="drivers.id", primary_key=True)
    lap: int = Field(..., primary_key=True)
    position: int
    time: int


class Pitstops(SQLModel, table=True):
    race_id: int = Field(..., foreign_key="races.id", primary_key=True)
    driver_id: int = Field(..., foreign_key="drivers.id", primary_key=True)
    stop: int = Field(..., primary_key=True)
    lap: int
    time: int
