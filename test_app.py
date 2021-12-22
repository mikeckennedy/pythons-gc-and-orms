import datetime
import gc
import os

from data.mongo import mongo_setup
from data.mongo.some_entry import SomeEntry as MongoEntry
from data.sql import db_session
from data.sql.some_entry import SomeEntry as SqlEntry
from importer import importer


def main():
    setup_sql()
    setup_mongo()

    test_sql(1)
    test_mongodb(1)

    q = input("Run with [d]efault GC settings? Or [o]ptimized GC settings? ")
    if q not in {'d', 'o'}:
        print("You must pick d or o for options")
        exit(-1)

    alter = (q == 'o')

    q = input("Show GC diagnostics (slower) [y]es/[n]o? ")
    if q not in {'y', 'n'}:
        print("You must pick y or n for options")
        exit(-1)

    diags = (q == 'y')

    config_gc(alter, diags)

    q = input("Test [M]ongoDB or [S]QLAlchemy? ")
    if q.lower() not in {'m', 's'}:
        print("You must pick m or s for options")
        exit(-1)

    if q == 's':
        test_sql(importer.ENTRY_COUNT / 5)
    elif q == 'm':
        test_mongodb(importer.ENTRY_COUNT/5)

    input('Done, check mem then hit enter to exit: ')


def config_gc(alter: bool, diags: bool):
    # Clean up what might be garbage
    gc.collect(2)
    # Exclude current items from future GC.
    gc.freeze()

    # Turn on to see GC numbers, but slows things down a tad.
    if diags:
        print("Enabling GC diagnostics (slower)...")
        gc.set_debug(gc.DEBUG_STATS)

    if alter:
        print("Altering default GC behavior")
        allocations, gen1, gen2 = gc.get_threshold()
        allocations = 50_000  # Start the GC sequence every 50K not 700 class allocations.
        gc.set_threshold(allocations, gen1, gen2)
        print(f"GC set to: {allocations:,}, {gen1}, {gen2}.")
    else:
        allocations, gen1, gen2 = gc.get_threshold()
        print(f"Using Python's default GC config: {allocations:,}, {gen1}, {gen2}.")


def test_sql(count):
    t0 = datetime.datetime.now()
    s = db_session.create_session()
    try:
        if s.query(SqlEntry).count() == 0:
            print(f"ERROR: No SQL data found, run importer first.")
            return

        entries = []
        for e in s.query(SqlEntry):
            if len(entries) >= count:
                break

            entries.append(e)

        t1 = datetime.datetime.now()
        dt = (t1 - t0)
        print(f"Loaded {len(entries):,} entries from SQL. Time: {dt.total_seconds():,.3} sec", flush=True)
    finally:
        s.close()


def test_mongodb(count):
    t0 = datetime.datetime.now()
    if MongoEntry.objects().count() == 0:
        print(f"ERROR: No MongoDB data found, run importer first.")
        return

    entries = []
    for e in MongoEntry.objects():
        if len(entries) >= count:
            break

        entries.append(e)

    t1 = datetime.datetime.now()
    dt = (t1 - t0)
    print(f"Loaded {len(entries):,} entries from MongoDB. Time: {dt.total_seconds():,.3} sec", flush=True)


def setup_sql():
    db_file = os.path.join(
        os.path.dirname(__file__),
        '',
        'db',
        'gc_test_db.sqlite')

    db_session.global_init(db_file)


def setup_mongo():
    mongo_setup.global_init()


if __name__ == '__main__':
    main()
