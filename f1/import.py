import csv
import logging
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import sqlmodel as sm
from psycopg2.errors import UniqueViolation
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from f1 import models
from f1.db import engine

logger = logging.getLogger("f1.import")

DATA_DIR = Path(__file__).parent.parent / "data"

if not DATA_DIR.is_dir():
    raise Exception("Not a directory: {}".format(DATA_DIR))


class FieldMap(BaseModel):
    meth: Optional[Callable]
    fields: List[str]


class ModelMap(BaseModel):
    name: str
    filename: str
    id_field: Optional[str]
    model: str
    map: Dict[str, Union[str, FieldMap]]


join_starttimes = lambda x: "T".join(x)

# Models import map
_MODELS = [
    {
        "name": "circuits",
        "model": "Circuits",
        "filename": "circuits.csv",
        "id_field": "circuitId",
        "map": {
            "id": "circuitId",
            "code": "circuitRef",
            "name": "name",
            "location": "location",
            "country": "country",
            "altitude": "alt",
            "url": "url",
        },
    },
    {
        "name": "drivers",
        "model": "Drivers",
        "filename": "drivers.csv",
        "id_field": "driverId",
        "map": {
            "id": "driverId",
            "code": "driverRef",
            "number": "number",
            "acronym": "code",
            "name_first": "forename",
            "name_last": "surname",
            "dob": "dob",
            "nationality": "nationality",
            "url": "url",
        },
    },
    {
        "name": "constructors",
        "model": "Constructors",
        "filename": "constructors.csv",
        "id_field": "constructorId",
        "map": {
            "id": "constructorId",
            "code": "constructorRef",
            "name": "name",
            "nationality": "nationality",
            "url": "url",
        },
    },
    {
        "name": "races",
        "model": "Races",
        "filename": "races.csv",
        "id_field": "raceId",
        "map": {
            "id": "raceId",
            "year": "year",
            "round": "round",
            "circuit_id": "circuitId",
            "name": "name",
            "start": FieldMap(**{"meth": join_starttimes, "fields": ["date", "time"]}),
            "url": "url",
        },
    },
    {
        "name": "results_status",
        "model": "ResultsStatus",
        "filename": "status.csv",
        "id_field": "statusId",
        "map": {"id": "statusId", "status": "status"},
    },
    {
        "name": "results",
        "model": "Results",
        "filename": "results.csv",
        "id_field": "resultId",
        "map": {
            "id": "resultId",
            "race_id": "raceId",
            "driver_id": "driverId",
            "constructor_id": "constructorId",
            "status_id": "statusId",
            "number": "number",
            "grid": "grid",
            "position": "position",
            "position_status": "positionText",
            "position_order": "positionOrder",
            "points": "points",
            "laps": "laps",
            "time": "milliseconds",
        },
    },
    {
        "name": "laps",
        "model": "Laps",
        "filename": "lap_times.csv",
        "id_field": None,
        "map": {
            "race_id": "raceId",
            "driver_id": "driverId",
            "lap": "lap",
            "position": "position",
            "time": "milliseconds",
        },
    },
    {
        "name": "pitstops",
        "model": "Pitstops",
        "filename": "pit_stops.csv",
        "id_field": None,
        "map": {
            "race_id": "raceId",
            "driver_id": "driverId",
            "stop": "stop",
            "lap": "lap",
            "time": "milliseconds",
        },
    },
]


def _gen_model_map() -> Dict[str, ModelMap]:
    _models = {str(i["name"]): ModelMap(**i) for i in _MODELS}
    return _models


MODEL_MAP = _gen_model_map()


def import_model_map(model_map: ModelMap) -> None:
    file_path = DATA_DIR / model_map.filename

    records = []
    records_added = 0
    records_updated = 0
    records_error = 0

    with file_path.open() as fh:
        reader = csv.DictReader(fh)
        records = list(reader)

    with Session(engine) as sess:
        for record in records:
            # id value
            if model_map.id_field and model_map.id_field not in record:
                raise Exception("No id field {} in record".format(model_map.id_field))

            _id_value = None

            if model_map.id_field:
                _id_value = record[model_map.id_field]

            # get the model
            model_map_model = getattr(models, model_map.model)

            # find if its in the database
            model = None

            if _id_value:
                model = sess.query(model_map_model).get(_id_value)

            # basic record cleaning
            for k, v in record.items():
                if v == "\\N":
                    record[k] = None

                    if k == "time":
                        record[k] = "00:00:00"

            if not model:
                _value_dict = {
                    k: record[v] for k, v in model_map.map.items() if not isinstance(v, FieldMap)
                }
                model = model_map_model(**_value_dict)
                records_added += 1
            else:

                for k, v in model_map.map.items():
                    if k in ["id"]:
                        continue

                    if not isinstance(record[v], FieldMap):
                        setattr(model, k, record[v])

                records_updated += 1

            # do field maps
            for k, v in model_map.map.items():
                if isinstance(v, FieldMap):
                    _field_value = v.meth([record[i] for i in v.fields])
                    setattr(model, k, _field_value)

            try:
                sess.add(model)
                sess.commit()
            except (IntegrityError, UniqueViolation):
                records_error += 1
                sess.rollback()

    print(
        "Added {} and updated {} {} records with {} errors".format(
            records_added, records_updated, model_map.name, records_error
        )
    )


if __name__ == "__main__":
    import_model_map(MODEL_MAP["laps"])
