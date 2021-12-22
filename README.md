# Does Python do extremely too many GCs for ORMs?

## YES, OMG YES

Imagine you need to query a hefty number of records back from the database.
The sample app in this repo will create a database of 100,000 small records (see `importer.py`)
and then run a query that results in 20,000 being loaded into a single list (see `test_app.py`).

That's a lot, but not entirely out of bound of reasonable for certain problem sets.

During the execution of that single query against either SQLAlchemy or MongoEngine,
without adjusting Python's GC settings, we get an extreme number of GC collections 
(1,859 GCs for a single SQLAlchemy query). Yet, clearly none of these records are
garbage yet because they haven't even been fully realized from the DB.

Our fix at [Talk Python](https://talkpython.fm) has been to change the number of allocations required to *force*
a GC from 700 to 50,000. Interesting, this results in LESS not more memory used. 

The stats below are from Python 3.10.1 running on macOS with Apple Silicon.

## Python Default GC Settings

- SQLAlchemy - 20,000 records in one query
  - **1,859 GCs**
  - 908ms
  - 78.7 MB mem

- MongoEngine - 20,000 records in one query
  - **463 GCs**
  - 593ms
  - 75.8 MB mem


## Talk Python-optimized GC Settings

- SQLAlchemy - 20,000 records in one query: 
  - **29 GCs (64x improvement)**
  - 695ms (23% improvement)
  - 76.8 MB mem (surprisingly: 2% improvement with less GC)
- 
- MongoEngine - 20,000 records in one query
  - **10 GCs (46x improvement)**
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

## Resolutions

What can be done to improve this? 

Maybe someday Python will have an adaptive GC where if it runs a 
collection and finds zero cycles it backs off and if it starts finding more cycles it ramps up or 
something like that. Until then, we have a few knobs.

In Python,we have the `gc` module. This code will allow us to turn down the frequency of GCs:

```python
allocations, gen1, gen2 = gc.get_threshold()
allocations = 50_000  # Start the GC sequence every 50K not 700 class allocations.
gc.set_threshold(allocations, gen1, gen2)
```

Our experience running this code in production over at Talk Python ([podcast](https://talkpython.fm/) 
and [training site](https://training.talkpython.fm/)) has only been positive: Nearly unchanged memory usage
and significant performance improvements for just three lines of code.

Of course, this is a specific use-case: Web pages and APIs that return a non-trivial number of DB objects
(MongoEngine documents in our case) that are short-lived. Please test, profile, and monitor your code if you 
want to try this in your app.
