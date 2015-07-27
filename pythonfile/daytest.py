#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib

class Test:
    cursor_payRecord = None
    cursor_taskMoney = None
    cursor_giftRecord = None
    connection = None
    payRecord_map = {}
    taskMoney_map = {}
    giftRecord_map = {}
    pay_allprice = 0
    pay_allpeople = 0
    task_allprice = 0
    task_allpeople = 0
    gift_allprice = 0
    gift_allpeople = 0
    loss_price = 0
    def __init__(self, connection):
        self.connection = connection
    def release(self):
        if self.connection is not None:
            self.connection = None
            self.cursor_payRecord = None
            self.cursor_taskMoney = None
            self.cursor_giftRecord = None
    def getpayrecord(self, start, end):
        con = {
            "ctime": {
                    "$gte": start,
                    "$lte": end
            },
            "gameStatus": "ok",
            "alipayStatus": "ok",
            "type": "zhangyu"
        }
        return self.connection.get("payRecord", con)
    def gettaskmoney(self, start, end):
        con = {
            "ctime": {
                "$gte": start,
                "$lte": end
            }
        }
        return self.connection.get("taskMoney", con)
    def getgiftrecord(self, start, end):
        con = {
            "ctime": {
                "$gte": start,
                "$lte": end
            }
        }
        return self.connection.get("giftRecord", con)
    def payrecord(self,start, end):
        self.cursor_payRecord = self.getpayrecord(start, end)
        for cu in self.cursor_payRecord:
            num = cu.get("num")
            uid = cu.get("uid")
            if uid in self.payRecord_map.keys():
                self.payRecord_map[uid][0] += num
                self.payRecord_map[uid][1] += 1
            else:
                self.payRecord_map[uid] = [num, 1]
    def taskmoney(self, start, end):
        self.cursor_taskMoney = self.gettaskmoney(start, end)
        for cu in self.cursor_taskMoney:
            type_taskmoney = cu.get("type")
            status = cu.get("status")
            num = 0
            uid = cu.get("uid")
            if type_taskmoney == "mobile" and status == 2:
                num = 5000
            elif type_taskmoney == "sign":
                num = 100
            elif type_taskmoney == "regist":
                num = 1000
            if uid in self.taskMoney_map.keys():
                self.taskMoney_map[uid][0] += num
                self.taskMoney_map[uid][1] += 1
            else:
                self.taskMoney_map[uid] = [num, 1]
    def giftrecord(self, start, end):
        self.cursor_giftRecord = self.getgiftrecord(start, end)
        for cu in self.cursor_giftRecord:
            uid = cu.get("uid")
            price = cu.get("price")
            if uid in self.giftRecord_map.keys():
                self.giftRecord_map[uid][0] += price
                self.giftRecord_map[uid][1] += 1
            else:
                self.giftRecord_map[uid] = [price, 1]

    def query(self):
        for uid in self.payRecord_map.keys():
            self.pay_allprice += self.payRecord_map[uid][0]
            self.pay_allpeople += 1
        for uid in self.taskMoney_map.keys():
            self.task_allprice += self.taskMoney_map[uid][0]
            self.task_allpeople += 1
        for uid in self.giftRecord_map.keys():
            self.gift_allprice += self.giftRecord_map[uid][0]
            self.gift_allpeople += 1
        self.loss_price = self.pay_allprice - self.gift_allprice

    def runTest(self, start, end):
        if self.connection is None:
            print "the connection is None"
            return
        self.payrecord(start, end)
        self.taskmoney(start, end)
        self.giftrecord(start, end)
        self.query()
        self.release()
    def printresult(self):
        print "充值章鱼币的总价值： ", self.pay_allprice
        print "充值的总人数： ", self.pay_allpeople
        print "任务领取章鱼币的总价值： ", self.task_allprice
        print "任务领取的总人数： ", self.task_allpeople
        print "送出礼物的总价值： ", self.gift_allprice
        print "送出礼物的总人数： ", self.gift_allpeople
        print "亏损值： ", self.loss_price

    def postdb(self):
        url = "http://feedback.kukuplay.com/datamonitor/feedbackUpdate"
        value = {
            "app": "daytest",
            "data": {
                "pay_allprice": self.pay_allprice,
                "pay_allpeople": self.pay_allpeople,
                "task_allprice": self.task_allprice,
                "task_allpeople": self.task_allpeople,
                "gift_allprice": self.gift_allprice,
                "gift_allpeople": self.gift_allpeople,
                "loss_price": self.loss_price
            }
        }
        data = urllib.urlencode(value)
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(request)
        msg = response.read()
        print msg