#!/usr/bin/env python
# -*- coding: utf-8 -*-

class string:
    @staticmethod
    def strcpy(sou):
        tmp = sou
        if sou is None:
            return None
        if type(sou) is not str:
            tmp = str(sou)
        return tmp
    @staticmethod
    def strcat(str1, str2):
        tmp = str1+str2
        return tmp
    @staticmethod
    def strfind(source, destination):
        index = source.index(destination)
        return index
    @staticmethod
    def strcmp(source, destination):
        re = cmp(source, destination)
        return re
    @staticmethod
    def strncat(source, destination, n):
        l = len(destination)
        if n <= l:
            l = n
        tmp = source+destination[0:l]
        return tmp
    @staticmethod
    def strncmp(str1, str2, n):
        len1 = len(str1)
        len2 = len(str2)
        if n <= len1:
            len1 = n
        if n <= len2:
            len2 = n
        re = cmp(str1[0:len1], str2[0:len2])
        return re
    @staticmethod
    def strreplace(source, str1, str2):
        if str2 is None:
            return source
        strlist = source.split(str1)
        tmp = ""
        for s in strlist:
            tmp = tmp+s+str2
        length = len(tmp)
        return tmp[0:length-len(str2)]
    @staticmethod
    def strrev(str1):
        tmp = str1[::-1]
        return tmp


