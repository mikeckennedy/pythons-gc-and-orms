# Question: Does Python do extremely too many GCs for ORMs?

## YES, OMG YES. Check this out

**Python Default GC Settings**:

- SQLAlchemy - 20,000 records in one query
  - **1,859 GCs**
  - 908ms
  - 78.7 MB mem

- MongoDB - 20,000 records in one query
  - 463 GCs
  - 593ms
  - 75.8 MB mem


**Talk Python-optimized GC Settings**:

- SQLAlchemy - 20,000 records in one query: 
  - **29 GCs (64x improvement)**
  - 695ms (23% improvement)
  - 76.8 MB mem (surprisingly: 2% improvement with less GC)
- 
- MongoDB - 20,000 records in one query
  - 10 GCs (46x improvement)
  - 515ms (13%)
  - 72.3 MB mem (surprisingly: 4% improvement with less GC)
