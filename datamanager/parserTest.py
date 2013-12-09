#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys, os
import urllib2
import zmq
import thread
import time
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.abspath('../databaseinfo')))
from databaseinfo import queryOnTable, confTableAttr
from parser import extractTitle, extractDate, extract_content_with_Arc90


#doUrl = "http://sports.news.naver.com/sports/index.nhn?category=worldbaseball&ctg=news&mod=read&office_id=422&article_id=0000030509&date=20131010&page=2"
doUrl = "http://sports.media.daum.net/worldbaseball/news/breaking/view.html?cateid=1015&newsid=20131010155109523&p=newsis"
defaultStatus = 200
req = urllib2.Request(doUrl)
try :
    response = urllib2.urlopen(req).read()
except urllib2.URLError as e:
    print "온라인 연결 되어있나요? " + str(e.reason)
except urllib2.HTTPError as e:
    print e.code
soup = BeautifulSoup(str(response))
infoTitle = extractTitle(soup)
infoDate = extractDate(soup)
infoBody = extract_content_with_Arc90(str(response))

print infoTitle
print infoDate
print infoBody
