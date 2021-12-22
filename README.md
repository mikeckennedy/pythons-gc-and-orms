# Question: Does Python do extremely too many GCs for ORMs?

## YES, OMG YES. Check this out

Imagine you need to query a hefty number of records back from the database.
The sample app in this repo will create a database of 100,000 small records (see `importer.py`)
and then run a query that results in 20,000 being loaded into a single list (see `test_app.py`).

That's a lot, but not entirely out of bound of reasonable for certain problem sets.

During the execution of that single query against either SQLAlchemy or MongoEngine,
without adjusting Python's GC settings, we get an extreme number of GC collections 
(1,859 GCs for a single SQLAlchemy query). Yet, clearly none of these records are
garbage yet because they haven't even been fully realized from the DB.

Our fix at Talk Python has been to change the number of allocations required to *force*
a GC from 700 to 50,000. Interesting, the results in LESS not more memory used. 

The stats below are from Python 3.10.1 running on macOS with Apple Silicon.

## Python Default GC Settings

- SQLAlchemy - 20,000 records in one query
  - **1,859 GCs**
  - 908ms
  - 78.7 MB mem

- MongoEngine - 20,000 records in one query
  - 463 GCs
  - 593ms
  - 75.8 MB mem


## Talk Python-optimized GC Settings

- SQLAlchemy - 20,000 records in one query: 
  - **29 GCs (64x improvement)**
  - 695ms (23% improvement)
  - 76.8 MB mem (surprisingly: 2% improvement with less GC)
- 
- MongoEngine - 20,000 records in one query
  - 10 GCs (46x improvement)
  - 515ms (13%)
  - 72.3 MB mem (surprisingly: 4% improvement with less GC)

## Running the app

1. Create a virtual environment: `python3 -m venv venv`
2. Activate it: `. /venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Import the data: `python importer/importer.py`
5. Run the test query app: `python test_app.py`
6. Choose combinations of the different options offered in the app
7. Count the number of times `"gc: done"` appears when running with diagnostics on
