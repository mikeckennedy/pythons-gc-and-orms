import datetime
import random
import uuid

import sqlalchemy

from data.sql.modelbase import SqlAlchemyBase


class SomeEntry(SqlAlchemyBase):
    __tablename__ = 'some_entries'

    id: str = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    some_random_number: int = sqlalchemy.Column(sqlalchemy.Integer, default=lambda: random.randint(1, 10_000))
