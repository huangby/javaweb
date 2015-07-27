#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from util.mongo import MongoClient
# from search import Search
from daytest import Test
# from redpacket import RedPacket
from convertion import Rate
import time

try:
    jf = open("config_db.json")
except IOError:
    print "Don't exist the file config_db.json"
config_json = json.load(jf)
con = MongoClient(config_json["host"], config_json["port"], config_json["dbname"])
re = con.authenticate(config_json["user"], config_json["passwd"])
if re is not True:
    print "Connection is fail"
jf.close()
# s = Search()
# s.mys(con, "giftRecord", {"ctime": {"$gte": begintime, "$lte": endtime}})
# s.printvalue()
# s.myfind(con)
# s.printvalue2()
def translatetime(timestr):
    '''
    :param timestr: {int,float,string}
    :return: { int 13bit}
    '''
    if timestr is None:
        return 0
    if type(timestr) is float or type(timestr) is int:
        return int(timestr) * 1000
    if type(timestr) is str:
        c = long(time.mktime(time.strptime(timestr, '%Y%m%d'))) * 1000
        return c
#dayStr 20150721 / 1 / 1452457859(123)
# def dealTime(dayStr):
#     tar_timestamp  = dayStr
#     return tar_timestamp
#
# day = int(time.time())
# start = dealTime(day-24*3600*1000)
# end = dealTime(day)
now = time.time()
start = translatetime(now - 7 * 24 * 3600)
end = translatetime(now - 6 * 24 * 3600)
# start = translatetime("2015720")
# end = translatetime("2015721")
day = Test(con)
day.runTest(start, end)
day.printresult()
# day.postdb()
day.release()

# red = RedPacket(con)
# red.calculatevalue()
# red.printvalue()
# red.release()
# now = time.time()
# start = translatetime(now - 7 * 24 * 3600)
# end = translatetime(now)
# rate = Rate(con)
# rate.runRate(start, end)
# getgift_rate, notget_rate = rate.getResult()
# print "完成任务并且领取钱的转化率：", getgift_rate
# print "完成任务但是没有领取钱的转化率：", notget_rate





