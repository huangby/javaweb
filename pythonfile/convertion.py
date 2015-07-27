#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Rate():
    red_num = 0
    rec_num = 0
    rec_not_num = 0
    cur_redpacketrecord = None
    cur_taskmoney = None
    redpacketrecord_uid_map = {}
    taskmoney_rec_uid_map = {}
    taskmoney_no_rec_uid_map = {}
    rec_uid_count = 0
    no_rec_uid_count = 0
    redpacketrecord_uid_count = 0
    receive_money_rate = 0
    no_receive_money_rate = 0
    connection = None
    def __init__(self, connection):
        self.connection = connection

    def getRedpacketReocrds(self, start, end):
        cond = {
            "ctime": {
                "$gte": start,
                "$lte": end
            },
            "rptype": "admin",
            "status": "success"
        }
        return self.connection.get("redpacketrecord", cond)

    def getTaskMoney(self, start, end):
        cond = {
            "type": "mobile",
            "ctime": {
                "$gte": start,
                "$lte": end
            }
        }
        return self.connection.get("taskMoney", cond)

    def release(self):
        if self.connection is not None:
            self.connection = None

    def calRedpacket(self, s, e):
        self.cur_redpacketrecord = self.getRedpacketReocrds(s, e)
        for cu in self.cur_redpacketrecord:
            uid = cu.get("uid")
            if uid in self.redpacketrecord_uid_map.keys():
                self.redpacketrecord_uid_map[uid] += 1
            else:
                self.redpacketrecord_uid_map[uid] = 1

    def calTaskMoney(self, s, e):
        self.cur_taskmoney = self.getTaskMoney(s, e)
        for cu in self.cur_taskmoney:
            status = cu.get("status")
            uid = cu.get("uid")
            if uid in self.redpacketrecord_uid_map.keys():
                if status == 1:
                    self.taskmoney_no_rec_uid_map[uid] = 1
                elif status == 2:
                    self.taskmoney_rec_uid_map[uid] = 1

    def calculate_result(self):
        self.rec_uid_count = len(self.taskmoney_rec_uid_map.keys())
        self.no_rec_uid_count = len(self.taskmoney_no_rec_uid_map.keys())
        self.redpacketrecord_uid_count = len(self.redpacketrecord_uid_map.keys())
        if self.redpacketrecord_uid_count == 0:
            self.receive_money_rate = 0
            self.no_receive_money_rate = 0
        else:
            self.receive_money_rate = float(self.rec_uid_count) / float(self.redpacketrecord_uid_count)
            self.no_receive_money_rate = float(self.no_rec_uid_count) / float(self.redpacketrecord_uid_count)

    def getResult(self):
        return [self.receive_money_rate, self.no_receive_money_rate]
    def runRate(self, s, e):
        self.calRedpacket(s, e)
        self.calTaskMoney(s, e)
        self.calculate_result()

