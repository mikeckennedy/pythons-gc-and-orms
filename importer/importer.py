import os
import sys
from typing import Final

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

from data.mongo import mongo_setup
from data.sql import db_session
from data.sql.some_entry import SomeEntry as SqlEntry
from data.mongo.some_entry import SomeEntry as MongoEntry

ENTRY_COUNT: Final[int] = 100_000


def main():
    setup_sql()
    setup_mongo()

    populate_sql()
    populate_mongodb()


def populate_sql():
    s = db_session.create_session()
    try:
        count = s.query(SqlEntry).count()
        if count > 1:
            print(f"SQL already populated ({count:,} items), skipping.")
            return

        print(f'Adding {ENTRY_COUNT:,} SQL entries, ...', flush=True)
        for _ in range(0, ENTRY_COUNT):
            s.add(SqlEntry())

        print(f'Committing SQL entries...', flush=True, end=' ')
        s.commit()
        print('done.')

    finally:
        s.close()


def populate_mongodb():
    try:
        count = MongoEntry.objects().count()
        if count > 1:
            print(f"MongoDB already populated ({count:,} items), skipping.")
            return

        entries = []
        print(f'Adding {ENTRY_COUNT:,} Mongo entries...', flush=True)
        for _ in range(0, ENTRY_COUNT):
            entries.append(MongoEntry())

        print(f'Committing MongoDB entries...', flush=True, end=' ')
        MongoEntry.objects().insert(entries)
        print('done.')
    except Exception as x:
        print(f"ERROR: Could not populate MongoDB data - is it running locally? {x}")


def setup_sql():
    db_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'db',
        'gc_test_db.sqlite')

    db_session.global_init(db_file)


def setup_mongo():
    mongo_setup.global_init()


if __name__ == '__main__':
    main()
