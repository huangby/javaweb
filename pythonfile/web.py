#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'windows7'
import socket
import os


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8080))
sock.listen(10)
f = open("web.html", 'r')
while True:
    print "正在监听......"
    se, addr = sock.accept()
    print "获得连接......"
    se.send("GET / HTTP/1.1\n")
    se.send("Accept:text/html,application/xhtml+xml,*/*;q=0.8\n")
    se.send("Accept-Encoding:gzip,deflate,sdch\n")
    se.send("Accept-Language:zh-CN,zh;q=0.8,en;q=0.6\n")
    se.send("Cache-Control:max-age=0\n")
    se.send("Connection:keep-alive\n")
    se.send("Host:" + "localhost" + "\r\n")
    se.send("Referer:http://www.baidu.com/\n")
    se.send("user-agent: Googlebot\n\n")
    se.send("hello")