# Goal

Implement the algorithm suggested in the [blog](http://www.scylladb.com/2017/02/13/efficient-full-table-scans-with-scylla-1-6/) post

# Basic env

Python: 2.7.5

Scylladb: 1.6

# Start up
## step1: prepare the basic data
Before start the select process, you need to prepare some data:

```
1. create the keyspace:
CREATE KEYSPACE scylladata WITH replication = {‘class’: ‘SimpleStrategy’, ‘replication_factor’ : 1};

2. create an example table
use scylladata;
CREATE TABLE example (
    id bigint,
    ck int,
    v1 text,
    v2 text,
    PRIMARY KEY(id, ck)
);

3. insert some data
insert into example (id, ck, v1, v2) " values (1, 2, 'aa', 'bb')
```

## step2: start the select process

The command is :

```
python select_from_scylla.py
```

# Comments:

Currently, we put the result into result_queue in select_from_scylla.py.

It's unsafe if there are too many data item in the table 'example'.

