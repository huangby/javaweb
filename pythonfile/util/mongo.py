#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo

class MongoClient:
    """ mongodb client """
    def __init__(self, host = "localhost", port = 27017, dbName = "test", debug = False):
        self.host = host
        self.port = port
        self.conn = pymongo.MongoClient(host, port)

        self.db = self.conn[dbName]
        self.debug = debug
        if(debug):
            print "host: " + host
            print "port: " + str(port)
            print "dbName: " + dbName

    def authenticate(self, username, passwd):
        ret = self.db.authenticate(username, passwd)
        return ret

    def getDBInfo(self):
        return

    def getCollections(self):
        return self.db.collection_names()

    def insert(self, collection, doc):
        coll = self.db[collection]
        ret = coll.insert(doc)
        return ret

    def get_one(self, collection, condition, fields = None):
        coll = self.db[collection]
        return coll.find_one(condition, fields)

    def get(self, collection, condition, fields = None):
        coll = self.db[collection]
        cursor = coll.find(condition, fields)
        return cursor

    def update(self, collection, condition, operation, upsert=False, manipulate=False, safe=False, multi=False, _check_keys=False):
        coll = self.db[collection]
        ret = coll.update(condition, operation, upsert = upsert, manipulate=manipulate, safe=safe, multi=multi)
        return ret

    def remove(self, collection, condition):
        coll = self.db[collection]
        return coll.remove(condition)

    def next(self, cursor):
        try:
            obj = cursor.next()
        except StopIteration:
            return None
        return obj

