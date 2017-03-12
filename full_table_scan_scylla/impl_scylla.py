#!/usr/bin/env python
# coding: utf8

import random
import sys

from cassandra.cluster import Cluster


class ScyllaClient(object):
    def __init__(self, host=None, port=None):
        self.host = host if host else ['127.0.0.1']
        self.port = port if port else 9042
        (self.cluster, self.session) = \
            self._init_connection(self.host, self.port)

    @staticmethod
    def _init_connection(host=None, port=None):
        cluster = Cluster(host, port=port)
        session = cluster.connect()
        return cluster, session

    def get_host(self):
        return self.host

    def get_port(self):
        return self.port

    def set_keyspace(self, keyspace=None):
        if not keyspace:
            return False
        cql_cmd = "use %s" % keyspace
        self.execute_cql(cql_cmd)

    def execute_cql(self, cql_cmd=None):
        result = self.session.execute(cql_cmd)
        return result

if __name__ == "__main__":
    data_obj = ScyllaClient()
    data_obj.set_keyspace("scylladata")
    cmd = "TRUNCATE TABLE  example"
    data_obj.execute_cql(cmd)

    max_record = int(sys.argv[1]) if sys.argv[1] else 100
    print max_record
    for i in xrange(1, max_record):
        cmd = "insert into example (id, ck, v1, v2) " \
              "values (%s, 2, 'aa', 'bb')" % i
        data_obj.execute_cql(cmd)