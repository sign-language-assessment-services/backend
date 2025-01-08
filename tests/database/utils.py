import inspect
import pkgutil
from typing import Type

from sqlalchemy import func, select, Table
from sqlalchemy.orm import Session

import app.database.tables
from app.database.tables.base import DbBase


def table_count(db_session: Session, table: Type[DbBase]) -> int:
    return db_session.scalar(select(func.count()).select_from(table))


def get_all_table_names_from_tables_folder() -> set:
    declared_tables = set()
    for _, module_name, _ in pkgutil.iter_modules(app.database.tables.__path__):
        module = __import__(f"app.database.tables.{module_name}", fromlist=[module_name])
        for _, obj in inspect.getmembers(module):  # , inspect.isclass):
            if hasattr(obj, "__tablename__"):
                declared_tables.add(obj.__tablename__)
            elif isinstance(obj, Table):
                declared_tables.add(obj.name)
    return declared_tables
