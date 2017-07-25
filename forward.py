# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 12:25:42 2017

@author: Sqrpi
"""


import re
import string
import sys
import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
from lxml import etree
import time

#
#reload(sys)
#sys.setdefaultencoding('utf-8')


def pp(text):
    print text.encode('utf-8').decode('utf-8')

def pl(List):
    for item in List:
        pp(item)


def pltx(List):
    for item in List:
        pp(item.text)

cookie = {"Cookie": 'Your Cookie Here'}
'''
    获得cookie: chromeF12-Network, 登录微博, 打开weibo.cn, Name列点击weibo.cn, 复制Cookie项
    示例格式: _T_WM=0c6a2e5cd..... SSOLoginState=150090124
'''
maxPage = 300
pageId = 1
flag = 0
maxPage = 10
Dict = {} # key forwards value
'''
    maxPage最大页数可修改
    Dict 是最终结果, A:[B,C]表示A从B,C处转发两次.
    但是A转发B, B转发C会记做 A:[B]
'''
while pageId < maxPage:
    url = 'https://weibo.cn/repost/FdSmtlQKX?uid=2670306073&rl=1&page=%d' % (pageId)
    html = requests.get(url, cookies=cookie).content

    soup = BeautifulSoup(html, 'lxml')
    forwardList = soup.find_all('div', class_='c')[3:]
    if not html:
        sys.stdout.write('\rWarning 251: Account Banned, trying to reconnect %d,page %d\t\t\t' % (flag, pageId))
        time.sleep(20)
        if flag >= 50:
            sys.stdout.write('\nError 254, page %d, Connection Failed\n' % (pageId))
            flag = 0
            continue
        flag += 1
        continue
    for item in forwardList:
        m = item.find_all('a')
        if len(m) > 2:
            forer = m[0].text
            fored = m[1].text[1:]
        elif len(m) == 2:
            forer = m[0].text
            fored = u'更方更正的物理'
        if forer not in Dict:
            Dict[forer] = [fored]
        elif fored not in Dict[forer]:
            Dict[forer].append(fored)
    pageId += 1
    flag = 0
    sys.stdout.write('\rLoaded page %d\t\t\t\t\t' % (pageId))