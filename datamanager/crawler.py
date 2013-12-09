#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys, os
import urllib2
import zmq
import thread
import time
import hashlib
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.abspath('../databaseinfo')))
from databaseinfo import queryOnTable, confTableAttr
from parser import extractTitle, extractDate, extract_content_with_Arc90
from handleprocess import controlJob

threadControl = controlJob.ControlPoint()
numberThread = threadControl.threadCnt
leftThread = numberThread
lockThread = thread.allocate_lock()

class DaemonCon():
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://127.0.0.1:5000")

    def getCommand(self):
        msg = "GET"
        self.socket.send(msg)
        self.msg_get = self.socket.recv()
        listUrl = eval(self.msg_get)
        return listUrl

    def doneCommand(self, url):
        msg = "DONE:"+url
        self.socket.send(msg)
        self.msg_get = self.socket.recv()
        return True

    def closeCommand(self):
        self.socket.close()

def threadExit(id):
    global leftThread
    print 'thread %d is quitting' % id
    lockThread.acquire()
    leftThread -= 1
    lockThread.release()


def crawlUrlWorker(processNum, numberThread):

    sqlHandle = queryOnTable.DBQuery()
    tblConf = confTableAttr.confAttr()

    feederOffer = DaemonCon()
    doUrlList = feederOffer.getCommand()
    print 'thread %d is started' % processNum

    nCheckCnt = 0

    bTurn = True
    while len(doUrlList) != 0:
        for infoUrl in doUrlList:
            doUrl = "http://" + infoUrl
            print processNum, " ", doUrl
            defaultStatus = 200
            req = urllib2.Request(doUrl)
            try :
                response = urllib2.urlopen(req).read()
            except urllib2.URLError as e:
                print "온라인 연결 되어있나요? " + str(e.reason)
                continue
            except urllib2.HTTPError as e:
                print e.code
                defaultStatus = 400
                feederOffer.doneCommand(infoUrl)
                continue
            soup = BeautifulSoup(str(response))
            infoTitle = extractTitle(soup)
            infoDate = extractDate(soup)
            infoBody = extract_content_with_Arc90(str(response))

            urlSplitLine = infoUrl.split("/")
            host = urlSplitLine[0]
            path = "/"+"/".join(urlSplitLine[1:len(urlSplitLine)])

            mapBODYAttrs = tblConf.BODYAttrs
            mapBODYAttrs['Host'] = host
            mapBODYAttrs['Path'] = path
            mapBODYAttrs['Title'] = infoTitle.encode('utf-8')
            mapBODYAttrs['Body'] = infoBody.encode('utf-8')
            mapBODYAttrs['StatusCode'] = defaultStatus
            mapBODYAttrs['ExtractDate'] = tblConf.nowTime()
            mapBODYAttrs['CreateDate'] = infoDate
            mapBODYAttrs['InversedDate'] = tblConf.inverseTime(mapBODYAttrs['CreateDate'])
            tableIndex = long(hashlib.md5(infoUrl).hexdigest(), 16) % 2
            sInsertQry = sqlHandle.makeInsertQry("Body_"+str(tableIndex), mapBODYAttrs)
            try :
                sqlHandle.executeMapQry(sInsertQry, mapBODYAttrs)
            except Exception, e:
                if "Duplicate entry" in str(e):
                    nCheckCnt += 1
                bLook = threadControl.breakPoint(host,nCheckCnt)
                if not bLook:
                    bTurn = False
                    break
            threadControl.sleepPoint(host)
            feederOffer.doneCommand(infoUrl)
        if bTurn:
            doUrlList = feederOffer.getCommand()
        else:
            break
    feederOffer.closeCommand()
    threadExit(processNum)


if __name__ == '__main__':
    for workerNumber in range(numberThread) :
        try:
            thread.start_new_thread(crawlUrlWorker, (workerNumber, numberThread))
            time.sleep(0.1)
        except Exception, err:
            print err

    while leftThread:
        time.sleep(1)


