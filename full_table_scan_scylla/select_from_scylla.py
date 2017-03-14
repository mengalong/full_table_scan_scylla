#!/usr/bin/env python
# coding=utf8

import impl_scylla as scylladb
import sys

from cassandra.query import SimpleStatement
from multi_thread import MultiThread
from Queue import Queue


# the configuration of scylla
OPT_CONF = {
    'host': ['127.0.0.1'],
    'port': 9042,
    'keyspace': 'scylladata',
    'table': 'example'
}

# depends on the cluster size
CLUSTER_INFO = {
    'node_num': 1,
    'core_num': 4
}


class SelectExample(scylladb.ScyllaClient):
    def __init__(self, query_queue=None, result_queue=None):
        host = OPT_CONF.get('host', None)
        port = OPT_CONF.get('port', None)
        super(SelectExample, self).__init__(host, port)
        self.keyspace = OPT_CONF.get('keyspace', None)
        self.table = OPT_CONF.get('table', None)

        self.set_keyspace(self.keyspace)
        self.query_queue = query_queue
        self.result_queue = result_queue

    def select_data(self, query_queue):
        query_cmd = "select * from %s where token(id) >= %s and " \
                    "token(id) <= %s" % (self.table,
                                         query_queue[0],
                                         query_queue[1])
        statement = SimpleStatement(query_cmd)
        result = self.execute_cql(statement)
        return result

    def select_by_token(self, sid=None):
        while not self.query_queue.empty():
            sub_range = self.query_queue.get()
            try:
                result = self.select_data(sub_range)
            except Exception as err:
                self.query_queue.put(sub_range)
            # put result into result_queue
            self.result_queue.put(result)


class SelectRange(object):
    def __init__(self, queue=None, query_parallels=None):
        self.queue = queue
        self.query_parallels = query_parallels

    def init_range_section(self):
        range_sections = self.query_parallels * 100
        max_num = pow(2, 63)
        start = -(max_num - 1)
        end = max_num - 1
        step = (end - start)/range_sections

        for item in xrange(start+step, end, step):
            data = (start, item)
            self.queue.put(data)
            start = item + 1

        data = (start, end)
        self.queue.put(data)


if __name__ == "__main__":

    node_num = CLUSTER_INFO.get('node_num', 3)
    core_num = CLUSTER_INFO.get('core_num', 2)
    query_parallels = node_num * core_num * 3

    query_queue = Queue()
    try:
        # init the query range sections
        range_obj = SelectRange(queue=query_queue,
                                query_parallels=query_parallels)
        range_obj.init_range_section()
    except Exception as err:
        print("Init the sub-range failed for:%s" % err)
        sys.exit(1)

    result_queue = Queue()
    try:
        # init an scylldb obj
        select_obj = SelectExample(query_queue=query_queue,
                                   result_queue=result_queue)
    except Exception as err:
        print("Init the scylla connection failed for:%s" % err)
        sys.exit(1)

    try:
        # start multi threads and select data from scylladb
        threads = []
        for sid in xrange(1, query_parallels+1):
            thread_obj = MultiThread(sid, select_obj.select_by_token)
            thread_obj.start()
            threads.append(thread_obj)

        for thread_item in threads:
            thread_item.join()
    except Exception as err:
        select_obj.clean_up()
        print("Select from scylladb failed for:%s" % err)

    # if you want to access the result data, you can use like this:
    # while not result_queue.empty():
    #     datas = result_queue.get()
    #     for item in datas:
    #         print item

    select_obj.clean_up()
