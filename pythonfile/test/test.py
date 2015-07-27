#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from util.mongo import MongoClient

gift = {"1427966921511": 100, "1427966874087": 6000, "1428490257923": 28000, "1428490254236": 88000}  # giftId : price

def trantime(t):
    c = long(time.mktime(time.strptime(t,"%a %b %d %H:%M:%S %Y")))
    return c

def mytest(cursor):
    num_allVlue = 0
    num_disCountAllValue = 0
    num_numberOfPeople = len(cursor.distinct("uid"))
    num_numberOfGift = cursor.count()
    num_numberOfIp = 0
    uniqids = cursor.distinct("uniqid")
    allPeople = len(cursor.distinct("uid"))
    print "allpeople", allPeople
    all = cursor.count()
    num_numberOfUid = 0
    num_rateOfPeople = 0
    num_rateOfGift = 0
    ips = {}
    uids = {}
    uid = []

    for un in uniqids:
        uids[un] = []
        ips[un] = []
    for cu in cursor:
        num_allVlue = gift[cu.get("giftId")] + num_allVlue
        num_disCountAllValue = gift[cu.get("giftId")] - cu.get("price") + num_disCountAllValue
        if cu.get("hasSendRedPacket") is True:
            uid.append(cu.get("uid"))
        if cu.get("hasSendRedPacket") is True:
            num_rateOfGift += 1
        uids[cu.get("uniqid")].append(cu.get("uid"))
        ips[cu.get("uniqid")].append(cu.get("ip"))
    s = set(uid)
    num_rateOfPeople = len(s)
    ip = []
    id = {}
    for k in ips.keys():
        l = len(set(ips[k]))
        if l > 2:
            ip.append(l)
    for k in uids.keys():
        l = len(set(uids[k]))
        if l > 2:
            id[l] = set(uids[k])
    print "allValue: ", num_allVlue
    print "disCountAllValue: ", num_disCountAllValue
    print "numberOfPeople: ", num_numberOfPeople
    print "numberOfGift: ", num_numberOfGift
    print "numberOfIp: ", ip
    print "numberOfUid: ", id
    print "rateOfPeople: ", float(num_rateOfPeople)/float(allPeople)
    print "rateOfGift: ", float(num_rateOfGift)/float(all)

btime = trantime("Wed Jul 15 00:00:00 2015") * 1000
etime = trantime("Thu Jul 16 00:00:00 2015") * 1000


h = "db.ali.ppweb.com.cn"
p = 30000
dbname = "zhibo"
user = "rsource"
pwd = "rs@pw"

# h = "10.11.12.31"
# p = 27017
# dbname = "zhangyu"
# user = "test"
# pwd = "testpw"


mc = MongoClient(host=h, port=p, dbName=dbname)
re = mc.authenticate(user, pwd)
if re is False:
    print "sorry,it is fail"

con = {
    "ctime": {
        "$gte": btime, "$lte": etime
    }
}
cursor = mc.get("giftRecord", con)
mytest(cursor)




