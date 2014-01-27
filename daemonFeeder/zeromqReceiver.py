#!/usr/bin/python

# control url feeder whit protocol http 
import zmq
import Queue
import signal
import sys,os
from orderJob import QueueOrder

interrupted = False

# init first
def getUrlOrderQueue(flag):
    jobCreate = QueueOrder()
    urlJobList = jobCreate.MakeOrderJobList(flag)
    queueJob = Queue.Queue()
    for threadNumber in urlJobList.keys():
        queueJob.put(urlJobList[threadNumber])
    return queueJob

def updateProcessQueue(urllist):
    jobUpdate = QueueOrder()
    jobUpdate.updateProcess(urllist)

def doneProcessQueue(url):
    jobUpdate = QueueOrder()
    jobUpdate.doneProcess(url)

def signal_handler(signum, frame):
    global interrupted
    interrupted = True

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5000")

doingUrlList = getUrlOrderQueue(False)

while True:
    try :
        receivemsg = socket.recv()
    except zmq.ZMQError:
        signal.signal(signal.SIGINT, signal_handler)
        if interrupted:
            print "End Processing..."
        break
    except KeyboardInterrupt, e:
        print "End Processing..."
        break

    if str(receivemsg) == "GET":
        sendmsg = doingUrlList.get()
        updateProcessQueue(sendmsg)
        if doingUrlList.qsize() == 0:
            doingUrlList = getUrlOrderQueue(True)
        socket.send(str(sendmsg))
        #print "Send : ", str(sendmsg)
    else :
        if "DONE" in str(receivemsg):
            url = receivemsg.split(":")[1]
            doneProcessQueue(url)
        socket.send("TRUE")
        #print "Done : " + url


