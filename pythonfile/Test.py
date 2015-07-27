#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 1 字符串
from util.String import string


def myAtoi(str):
    maxint = 2147483647
    f = 1
    num = 0
    number = ['0','1','2','3','4','5','6','7','8','9']
    for i in str:
        if i is " ":
            continue
        if i is "-":
            f = -1
            continue
        if i in number:
            num = num * 10 +int(i)
        if num > maxint:
            return maxint * f
    return num * f


def longstr(s):
    if s is None:
        return ""
    if len(s) == 1:
        return s
    min_start = 0
    max_len = 1
    for i in range(len(s)):
        if len(s) - i <= max_len / 2:
            break
        j = i
        k = i
        while k < len(s) - 1 and s[k + 1] == s[k]:
            k += 1
       # i = k+1
        while k < len(s) - 1 and j > 0 and s[k + 1] == s[j - 1]:
            k += 1
            j -= 1
        new_len = k - j + 1
        if new_len > max_len:
            min_start = j
            max_len = new_len
    return s[min_start:min_start + max_len]
str1 = "hello ,my world My  name is hel ,and your is ?"
str2 = "hello ,my world nice to meet you"
str3 = ","
str_list = ['1', '2', '3', '4', '5', '6']
print str1.index("name")
print cmp(str1, str2)
print len(str1 and str2)
print str1.upper()
print str1 + str2[16:]
print str1[::-1]
print str1.find("is")
print str1.split()
print str3.join(str_list)
s = None

print string.strreplace(str1, "en", "ours")
print string.strrev("so do i")

# 2 map list 排序、拼接、抓换
dic1 = {"a": 1, "c": 3, "b": 2, "d": 4}
dic2 = {"x": 24, "y": 25, "z": 26}
print dict(dic1.items() + dic2.items())
print dict(dic1, **dic2)

d = dic2.copy()
d.update(dic1)
print d

str1 = '[{name:"zhangsan",age:34},{name:"lisi",age:23}]'
obj = eval(str1.replace('{', 'dict(').replace('}', ')').replace(':', '='))
print obj, type(obj)


sd = '{"name":"zhang","value":100}'
my = eval(sd)
print my, type(my)

a = [3, 2, 4, 5, 9]
for i, j in enumerate(a):
    print i, j

dic = {"hello": 10, "yes": 1, "no": 0}
print "hello is in dic", "hello" in dic
ls = longstr("ababab")
print ls

x = "hello"
print '\000''
# 3 .小题练习




# 4 range()

# for r in range(1,10):