#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import time
class RedPacket:
    connection = None
    cur_redpacket = None
    cur_redpacketrecord = None
    cur_giftrecord = None
    cur_payrecord = None
    cur_channel = None
    cur_money = None
    cur_withdrawrecord = None

    redpacket_allprice = 0
    received_redpacket_allprice = 0
    surplus_redpacket_allprice = 0
    back = 0

    random_redpacket_allprice = 0
    random_received_redpacket_allprice = 0
    random_surplus_redpacket_allprice = 0
    random_back = 0

    gift_redpacket_allprice = 0
    gift_received_redpacket_allprice = 0
    gift_surplus_redpacket_allprice = 0
    gift_back = 0

    gift_allprice = 0
    sendgift_allprice = 0
    sendgift_allprice_nofish = 0
    discount_allprice = 0

    charge = 0
    withdrawcash_ctime = 0
    withdrawcash_checktime = 0
    channel = 0
    user = 0
    redpacket_map = {}
    redpacketrecord_map = {}
    giftprice = {"1427966921511": 100, "1427966874087": 6000, "1428490257923": 28000, "1428490254236": 88000}
    def __init__(self, connect):
        self.connection = connect
    @staticmethod
    def trantime2(timestr):
        if timestr is None:
            return 0
        c = long(time.mktime(time.strptime(timestr, '%Y%m%d'))) * 1000
        return c
    def getcursor(self, collection, condition):
        if self.connection is None:
            return None
        return self.connection.get(collection, condition)
    def release(self):
        if self.connection is not None:
            self.connection = None
            self.cur_redpacket = None
    def get_redpacket_condition(self):
        btimestr = "20150720"
        etimestr = "20150721"
        begintime = self.trantime2(btimestr)
        endtime = self.trantime2(etimestr)
        con = {
            "ctime": {
                "$gte": begintime,
                "$lte": endtime
            }
        }
        return con
    def get_redpacketrecord_condition(self):
        btimestr = "20150720"
        etimestr = "20150721"
        begintime = self.trantime2(btimestr)
        endtime = self.trantime2(etimestr)
        con = {
             "ctime": {
                "$gte": begintime,
                "$lte": endtime
             },
             "status": "success"
        }
        return con
    def get_giftrecord_condition(self):
        btimestr = "20150720"
        etimestr = "20150721"
        begintime = self.trantime2(btimestr)
        endtime = self.trantime2(etimestr)
        con = {
             "ctime": {
                "$gte": begintime,
                "$lte": endtime
            }
        }
        return con
    def get_payrecord_condition(self):
        btimestr = "20150720"
        etimestr = "20150721"
        begintime = self.trantime2(btimestr)
        endtime = self.trantime2(etimestr)
        con = {
             "ctime": {
                 "$gte": begintime,
                 "$lte": endtime
             },
             "gameStatus": "ok",
             "alipayStatus": "ok",
             "type": "zhangyu"
        }
        return con
    def get_channel_condition(self):
        con = {
        }
        return con
    def get_withdrawrecord_condition(self):
        btimestr = "20150720"
        etimestr = "20150721"
        begintime = self.trantime2(btimestr)
        endtime = self.trantime2(etimestr)
        con = {
            "ctime": {"$gte": begintime, "$lte": endtime}
        }
        return con
    def calculatevalue(self):
        if self.connection is None:
            return
        self.cur_redpacket = self.getcursor("redpacket", self.get_redpacket_condition())
        self.cur_redpacketrecord = self.getcursor("redpacketrecord", self.get_redpacketrecord_condition())
        self.cur_giftrecord = self.getcursor("giftRecord", self.get_giftrecord_condition())
        self.cur_payrecord = self.getcursor("payRecord", self.get_payrecord_condition())
        self.cur_channel = self.getcursor("channel", self.get_channel_condition())
        self.cur_withdrawrecord = self.getcursor("withdrawRecord", self.get_withdrawrecord_condition())

        for cu in self.cur_redpacket:
            total_money = cu.get("total_money")
            type = cu.get("type")
            backmoney = cu.get("backmoney")
            if type == "random":
                self.random_redpacket_allprice += total_money
                self.random_back += backmoney
            elif type == "gift":
                self.gift_redpacket_allprice += total_money
                self.gift_back += backmoney
        self.redpacket_allprice = self.random_redpacket_allprice + self.gift_redpacket_allprice
        self.back = self.random_back + self.gift_back
        for cu in self.cur_redpacketrecord:
            rmb = cu.get("rmb")
            rptype = cu.get("rptype")
            if rptype == "random":
                self.random_received_redpacket_allprice += rmb
            elif rptype == "gift":
                self.gift_received_redpacket_allprice += rmb
        self.received_redpacket_allprice = self.random_received_redpacket_allprice + self.gift_received_redpacket_allprice
        self.surplus_redpacket_allprice = self.redpacket_allprice - self.received_redpacket_allprice - self.back
        self.gift_surplus_redpacket_allprice = self.gift_redpacket_allprice - self.gift_received_redpacket_allprice - self.gift_back
        self.random_surplus_redpacket_allprice = self.random_redpacket_allprice - self.random_received_redpacket_allprice - self.random_back
        for cu in self.cur_giftrecord:
            giftid = cu.get("giftId")
            price = cu.get("price")
            self.gift_allprice += self.giftprice[giftid]
            if giftid != "1427966921511":
                self.sendgift_allprice_nofish += price
            self.sendgift_allprice += price
        self.discount_allprice = self.gift_allprice - self.sendgift_allprice
        channel_map = {}
        for cu in self.cur_channel:
            uid = cu.get("_id")
            channel_map[uid] = ""
        for cu in self.cur_payrecord:
            uid = cu.get("uid")
            num = cu.get("num")
            if uid in channel_map.keys():
                self.channel += num
            self.charge += num
        self.user = self.charge - self.channel
        for cu in self.cur_withdrawrecord:
            num = cu.get("num")
            checktime = cu.get("checktime")
            if checktime is not None:
                self.withdrawcash_checktime += num
            self.withdrawcash_ctime += num
    def printvalue(self):
        print "发出红包的总价值", self.redpacket_allprice
        print "已经领取的红包的总价值", self.received_redpacket_allprice
        print "剩余红包的总价值", self.surplus_redpacket_allprice
        print "退回", self.back

        print "发出随机红包的总价值", self.random_redpacket_allprice
        print "已经领取的随机红包的总价值", self.random_received_redpacket_allprice
        print "剩余随机红包的总价值", self.random_surplus_redpacket_allprice
        print "随机红包的退回", self.random_back

        print "发出礼物红包的总价值", self.gift_redpacket_allprice
        print "已经领取的礼物红包的总价值", self.gift_received_redpacket_allprice
        print "剩余礼物红包的总价值", self.gift_surplus_redpacket_allprice
        print "礼物红包的退回", self.gift_back

        print "礼物总支出： ", long(self.gift_allprice) / long(1000)
        print "送出的礼物（包含鱿鱼串）： ", self.sendgift_allprice
        print "送出的礼物（不包含鱿鱼串）: ", self.sendgift_allprice_nofish
        print "礼物额外补贴", self.discount_allprice

        print "充值", long(self.charge) / long(1000)
        print "提现(按ctime)", long(self.withdrawcash_ctime) / long(1000)
        print "提现(按checktime)", long(self.withdrawcash_checktime) / long(1000)
        print "主播充值", long(self.channel) / long(1000)
        print "用户充值", long(self.user) / long(1000)
    def get_redpacket_postdata(self):
        value = {
            "app": "redpacket",
            "data": {
                "redpacket_allprice", self.redpacket_allprice,
                "received_redpacket_allprice", self.received_redpacket_allprice,
                "surplus_redpacket_allprice", self.surplus_redpacket_allprice,
                "back", self.back,
                "random_redpacket_allprice", self.random_redpacket_allprice,
                "random_received_redpacket_allprice", self.random_received_redpacket_allprice,
                "random_surplus_redpacket_allprice", self.random_surplus_redpacket_allprice,
                "random_back", self.random_back,
                "gift_redpacket_allprice", self.gift_redpacket_allprice,
                "gift_received_redpacket_allprice", self.gift_received_redpacket_allprice,
                "gift_surplus_redpacket_allprice", self.gift_surplus_redpacket_allprice,
                "gift_back", self.gift_back
            }
        }
        return value
    def get_gift_postdata(self):
        value = {
            "app": "redpacket",
            "data": {
                "gift_allprice": self.gift_allprice,
                "sendgift_allprice": self.sendgift_allprice,
                "sendgift_allprice_nofish": self.sendgift_allprice_nofish,
                "discount_allprice": self.discount_allprice
            }
        }
        return value
    def get_all_postdata(self):
        value = {
            "app": "redpacket",
            "data": {
                "charge": self.charge,
                "withdrawcash_ctime": self.withdrawcash_ctime,
                "withdrawcash_checktime": self.withdrawcash_checktime,
                "channel": self.channel,
                "user": self.user
            }
        }
        return value
    def postdb(self):
        url = "http://feedback.kukuplay.com/datamonitor/feedbackUpdate"

        value_redpacket = self.get_redpacket_postdata()
        value_gift = self.get_gift_postdata()
        value_all = self.get_all_postdata()

        data_redpacket = urllib.urlencode(value_redpacket)
        data_gift = urllib.urlencode(value_gift)
        data_all = urllib.urlencode(value_all)

        request = urllib2.Request(url, data_redpacket)
        response = urllib2.urlopen(request)
        msg = response.read()
        print msg
