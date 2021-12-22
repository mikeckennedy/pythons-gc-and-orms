import datetime
import random

import mongoengine


class SomeEntry(mongoengine.Document):
    created_date: datetime.datetime = mongoengine.DateTimeField(default=datetime.datetime.now)
    some_random_number: int = mongoengine.IntField(default=lambda: random.randint(1, 10_000))

    meta = {
        'db_alias': 'core',
        'collection': 'some_entries',
        'indexes': [
        ]
    }
