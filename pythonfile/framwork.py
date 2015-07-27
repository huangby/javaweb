#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import urllib
import urllib2

def trantime2(timestr):
    if timestr is None:
        return 0
    c = long(time.mktime(time.strptime(timestr, '%Y%m%d'))) * 1000
    return c
#
#
class Fram:
    connection = None
    def __init__(self):
        pass
    def getcursor(self, collection, condition):
        if self.connection is None:
            return None
        return self.connection.get(collection, condition)
    def release(self):
        if self.connection is not None:
            self.connection = None
    def printvalue(self):
        pass
    def get_postdata(self):
        value = {
            "app": "test"
        }
        return value
    def postdb(self):
        url = "http://feedback.kukuplay.com/datamonitor/feedbackUpdate"
        value = self.get_postdata()
        data = urllib.urlencode(value)
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(request)
        msg = response.read()
        print msg