# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 14:43:21 2018

@author: SQRPI/Ning Shangyi
"""

# -*- coding: utf-8 -*-


import sys
from bs4 import BeautifulSoup
import requests
import time
import argparse

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Cookie':'',
'Host':'weibo.cn',
'Referer':'https://weibo.cn/2113734951/profile',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
}


def readCookies(path):
    global cookieNum, cookieCount
    cookieCount = 0
    cookieNum = 0
    f = open(path, 'r')
    cookie = []
    flag = 0
    for line in f:
        if line.strip()[0] == '#':
            continue
        if flag==0:
            flag = 1
            if line.strip()=='':
                continue
        cookie.append(line.strip())
        cookieCount += 1
    if cookieCount == 0:
        raise Exception('Input your cookies in cookies.txt!')
    return cookie

def weiboContent(uid, pages=1, uidnum=1):
    global cookieNum, cookieCount, uidCount
    startCookie = 0
    flag = 0
    toReturn = []
    page = 0
    while page <= pages:
        try:
            headers['Cookie'] = cookie[cookieNum]
            url = 'https://weibo.cn/u/%s?page=%d' % (uid, page+1)
            s = requests.Session()
            s.headers.update(headers)
            html = s.get(url).content

            soup = BeautifulSoup(html, 'lxml')
            content = soup.find_all('span', {'class': 'ctt'})
            if page == 0 and len(content) >= 3:
                content = content[3:len(content)]
            for i in range(len(content)):
                toReturn.append([uid, page*10+i+1, content[i].getText()])
            if not html:
                if startCookie==0:
                    startCookie = cookieNum
                    cookieNum = (cookieNum + 1)%cookieCount
                    continue
                cookieNum = (cookieNum + 1)%cookieCount
                if cookieNum != startCookie:
                    continue
                sys.stdout.write('\rWarning: All Accounts Banned, trying to reconnect %d, uid %d/%d, page %d/%d' % (flag, uidnum, uidCount, page, args.p))
                time.sleep(20)
                if flag >= 50:
                    sys.stdout.write('\nError 254, uid =%s Page= %d, %d/1000, Connection Failed\n' % (uid, page, uidnum))
                    page += 1
                    flag = 0
                    continue
                flag += 1
                continue
            startCookie = 0
            page += 1
            flag = 0
            sys.stdout.write('\rLoaded %3d-th uid, Page %d/%d...\t\t\t\t\t\t\t\t' % (uidnum, page, pages+1))
        except:
            if flag:
                sys.stdout.write('\rWarning: uid =%s Page= %d, %d/1000, trying to reconnect %d\t\t\t\t\t' % (uid, page, uidnum, flag))
            time.sleep(20)
            if flag >= 50:
                sys.stdout.write('\nError: uid =%s PageId= %d, %d/1000, Connection Failed\n' % (uid, page, uidnum))
                page += 1
                flag = 0
                continue
            flag += 1
            continue
    return toReturn

def readUids(path):
    global uidCount
    uidCount = 0
    f = open(path, 'r')
    uids = []
    flag = 0
    for line in f:
        if line.strip()[0] == '#':
            continue
        if flag==0:
            flag = 1
            if line.strip()=='':
                continue
        uids.append(line.strip())
        uidCount += 1
    if uidCount == 0:
        raise Exception('Input your uids in uids.txt!')
    return uids
def writeContent(uids, text, pages):
    global uidCount
    start = False
    try:
        f = open(text, 'r')
        for line in f:
            pass
        contentNum = int(line.split('\t')[1])
        startUid = line.split('\t')[0]
        f.close()
    except:
        contentNum = 0
        startUid = uids[0]
    f = open(text, args.m)
    for i in range(len(uids)):
        if start is True:
            t = weiboContent(uids[i], pages, uidnum=i+1)
            for item in t:
                f.write('%s\t%d\t%s\n' % (item[0], item[1], item[2].decode('utf8')))
        if uids[i] == startUid:
            start = True
            sys.stdout.write('Started! uid = %s, content %d/%d\n' % (startUid, i+1, uidCount))
            t = weiboContent(uids[i], pages, uidnum=i+1)
            for item in t:
                    if item[1] >= contentNum:
                        f.write('%s\t%d\t%s\n' % (item[0], item[1], item[2]))
    f.close()
    return
    

parser  = argparse.ArgumentParser()
parser.add_argument('--p', type=int, default=20)
parser.add_argument('--f', type=str, default='result.txt')
parser.add_argument('--c', type=str, default='cookies.txt')
parser.add_argument('--u', type=str, default='uids.txt')
parser.add_argument('--m', type=str, default='a')
args    = parser.parse_args()
cookie  = readCookies(args.c)
uids    = readUids(args.u)
writeContent(uids, args.f, args.p-1)
sys.stdout.write('\nFinished!\n')
