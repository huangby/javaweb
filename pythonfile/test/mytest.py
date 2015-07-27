#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import urllib2
# response = urllib2.urlopen("http://jiaowu.buaa.edu.cn")
# html = response.read()
# print type(html)
# import time
# import calendar
#
# b = time.clock()
# t = time.asctime(time.localtime(time.time()))
# print t, type(t)
#
# cal = calendar.month(2015, 7)
# print cal
#
# e = time.clock()
# print e-b
#
# print type(time.time()), time.mktime(time.localtime(time.time()))
#
# tm = time.strptime(t, '%a %b %d %H:%M:%S %Y')
# print long(time.mktime(tm))
#
# ssss = 100
# print
# import urllib2
# req = urllib2.Request("http://www.baidu.com")  #
# respons = urllib2.urlopen(req)
# r = respons.read()
# open("D:\\baidu.html", 'w').write(r)

import time
a = "20150721"
x = time.mktime(time.strptime(a, '%Y%m%d'))
print x