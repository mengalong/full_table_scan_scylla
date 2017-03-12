#!/usr/bin/env python
# coding:utf8
from threading import Thread


class MultiThread(Thread):
    def __init__(self, sid=None, target=None):
        super(MultiThread, self).__init__()
        self.handle = target
        self.sid = sid

    def run(self):
        self.handle(self.sid)


def handle_it(*args):
    print "Test the handle"

if __name__ == "__main__":
    t = MultiThread(target=handle_it)
    t.start()
