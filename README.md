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

3. insert some data: You can execute cql via cqlsh:
insert into example (id, ck, v1, v2) " values (1, 2, 'aa', 'bb')

or execute the command:
cd full_table_scan_scylla/
python impl_scylla.py [row_num] 	# this will insert row_num rows data into the table scylladata.example
```

## step2: start the select process

The execute command is :

```
cd full_table_scan_scylla/
python select_from_scylla.py
```

# Comments:

Currently, we put the result into result_queue in select_from_scylla.py.

It's unsafe if there are too many data item in the table 'example'.

# Configurations:

In the file :full_table_scan_scylla/select_from_scylla.py, there are two public args like this:

```
# the configuration of scylla
OPT_CONF = {
    'host': ['127.0.0.1'],
    'port': 9042,
    'keyspace': 'scylladata',
    'table': 'example'
}
```

```
# depends on the cluster size
CLUSTER_INFO = {
    'node_num': 1,
    'core_num': 4
}
```

You can modify it in your case.

# Some test data:

data-scale|select time|
:---------|:----------|
10        |1.759
100       |2.568
1000      |2.815
10000     |2.166
100000    |3.574