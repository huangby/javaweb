#!/usr/bin/env python
# -*- coding: utf-8 -*-
from util.mongo import MongoClient
import time
def trantime(t):
    c = long(time.mktime(time.strptime(t,"%a %b %d %H:%M:%S %Y")))
    return c

ar = {"43": 1000}
h = "10.11.12.31"
p = 27017
dbname = "zhangyu"
user = "test"
passwd = "testpw"
m = MongoClient(host=h,port=p,dbName=dbname)
c = m.authenticate(user, passwd)
if c != True:
    print "fail"
con = {
}
g = m.get("money", con)
a = g.distinct("_id")
print len(a), g.count()
for gc in g:
    if gc.get("_id") in ar.keys():
        print ar[gc.get("_id")]



btime = trantime("Wed Jul 15 00:00:00 2015")
etime = trantime("Thu Jul 16 00:00:00 2015")

print btime,etime


