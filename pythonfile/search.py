#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
class Search:
    def __init__(self):
        self.num_allvalue = 0
        self.num_numberofpeople = 0
        self.num_numberofgift = 0
        self.allpeople = 0
        self.allgift = 0
        self.num_rateofgift = 0
        self.num_rateofpeople = 0
        self.num_discountallvalue = 0
        self.ip = []
        self.id = {}
        self.gift = {"1427966921511": 100, "1427966874087": 6000, "1428490257923": 28000, "1428490254236": 88000}
        self.charge_discount_gift_number = 0    # 充值 送过的个数
        self.charge_discount_people_number = 0  # 充值 送过的人数
        self.no_charge_discount_gift_number = 0
        self.no_charge_discount_people_number = 0
    def trantime2(self, timestr):
        # 20150715 -->1421551234
        t = (int(timestr[0:4]), int(timestr[4:6]), int(timestr[6:8]), 0, 0, 0, 0, 0, 0)
        c = long(time.mktime(t))
        return c

    def  getDatas(self, connection, collection, cond):
        cursor = connection.get(collection, cond)
        return cursor

    def mys(self, connection):
        cursor = self.getDatas(connection)
        self.num_numberofpeople = len(cursor.distinct("uid"))
        self.num_numberofgift = cursor.count()
        uniqids = cursor.distinct("uniqid")
        self.allpeople = len(cursor.distinct("uid"))
        self.allgift = cursor.count()

        ips = {}
        uids = {}
        uid = []
        for un in uniqids:
            uids[un] = []
            ips[un] = []
        for cu in cursor:
            giftid = cu.get("giftId")
            if giftid is not None:
                self.num_allvalue += self.gift[giftid]
                self.num_discountallvalue += self.gift[giftid] - cu.get('price')
            if cu.get("hasSendRedPacket") is True:
                uid.append(cu.get("uid"))
            if cu.get("hasSendRedPacket") is True:
                self.num_rateofgift += 1
            uniqid = cu.get("uniqid")
            if uniqid is not None:
                uids[uniqid].append(cu.get("uid"))
                ips[uniqid].append(cu.get("ip"))
                # #ip_lst
                # lst = ips.get(uniqid)
                # if lst is None:
                #     lst =[]
                # lst.append(uniqid)
                # ips[uniqid] =lst
                # #uid_lst

        s = set(uid)
        self.num_rateofpeople = len(s)
        for k in ips.keys():
            l = len(set(ips[k]))
            if l > 2:
                self.ip.append(l)
        for k in uids.keys():
            l = len(set(uids[k]))
            if l > 2:
                self.id[l] = set(uids[k])
    def myfind(self, connection):
        con_gift = {
            "ctime": {
                "$gte": long(self.trantime2("20150718")) * 1000,
                "$lte": long(self.trantime2("20150719")) * 1000
            }
        }
        cur_gift = self.getDatas(connection, "giftRecord", con_gift)
        con_money = {
            "moneyin": {
                "$gt": 0
            }
        }
        cur_money = self.getDatas(connection, "money", con_money)
        charge_uid_map = {}
        discount_map = {}     # 送过打折啤酒的
        not_discount_map = {}
        all_people_map = {}
        for cu in cur_gift:

            # price = cu.get("price")
            # uid = cu.get("uid")
            # uname=cu.get("uname")
            # all_people_map[uid]= uname
            #
            #

            if cu.get("price") == 3000:
                if cu.get("uid") in discount_map:
                    discount_map[cu.get("uid")] += 1
                else:
                    discount_map[cu.get("uid")] = 1
            else:
                if cu.get("uid") in not_discount_map:
                    not_discount_map[cu.get("uid")] += 1
                else:
                    not_discount_map[cu.get("uid")] = 1
            self.allgift += 1
        for cu in cur_money:
            if cu.get("_id") in discount_map:
                charge_uid_map[cu.get("_id")] = cu.get("moneyin")
        not_only_discount_number = 0
        discount_map_len = 0
        for k in discount_map.keys():
            if k in charge_uid_map.keys():
                self.charge_discount_people_number += 1
                self.charge_discount_gift_number += discount_map[k]
            else:
                self.no_charge_discount_people_number += 1
                self.no_charge_discount_gift_number += discount_map[k]
            if k in not_discount_map.keys():
                not_only_discount_number += 1
            discount_map_len += 1
        self.allpeople = discount_map_len + len(not_discount_map.keys()) - not_only_discount_number
    def printvalue(self):
        print "allValue: ", self.num_allvalue
        print "disCountAllValue: ", self.num_discountallvalue
        print "numberOfPeople: ", self.num_numberofpeople
        print "numberOfGift: ", self.num_numberofgift
        print "numberOfIp: ", self.ip
        print "numberOfUid: ", self.id
        print "rateOfPeople: ", float(self.num_rateofpeople)/float(self.allpeople)
        print "rateOfGift: ", float(self.num_rateofgift)/float(self.allgift)
    def printvalue2(self):
        print "未充值，送过3元礼物的人数", self.no_charge_discount_people_number
        print "未充值，送过3元礼物的个数", self.no_charge_discount_gift_number
        print "充值，送过3元礼物的人数", self.charge_discount_people_number
        print "充值，送过3元礼物的个数", self.charge_discount_gift_number
        print "送礼的人数", self.allpeople
        print "送礼的个数", self.allgift