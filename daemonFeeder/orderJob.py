import sys,os
sys.path.append(os.path.dirname(os.path.abspath('../databaseinfo')))
from databaseinfo import queryOnTable
import Queue

class QueueOrder(object):

    def MakeOrderJobList(self, condition):

        divideOrderList = 4
        threadWorker = {}
        orderedMap = {}
        getDataHandler = queryOnTable.DBQuery()
        if condition:
            orderedQry = "select host, path, priority from ListURL where processcondition = 0 order by priority desc, inverseddate"
        else:
            orderedQry = "select host, path, priority from ListURL where processcondition != 2 order by priority desc, inverseddate"

        self.receiveData = getDataHandler.selectQry(orderedQry)
        self.returnthreadWorker = {}
        self.returnthreadCnt = divideOrderList

        for rec in self.receiveData:
            url = rec['host'] + rec['path']

            if orderedMap.has_key(rec['host']):
                pass
            else:
                orderedMap[rec['host']] = Queue.Queue()

            orderedMap[rec['host']].put(url)

        splitTotalSize = 0
        sizeCaseQueue = {}
        for siteName in orderedMap:
            sizeCaseQueue[siteName] = orderedMap[siteName].qsize()
            splitTotalSize = splitTotalSize + sizeCaseQueue[siteName]

        splitDivideSize = (splitTotalSize / divideOrderList) + 1

        sortedCase = sorted(sizeCaseQueue.items(), key=lambda x:x[1], reverse=True)

        threadIndex = 0
        threadWorker[threadIndex] = []
        workCnt = 1
        for siteNameVal in sortedCase:
            siteName = siteNameVal[0]
            while not orderedMap[siteName].empty():
                threadWorker[threadIndex].append(orderedMap[siteName].get())
                if splitDivideSize == workCnt:
                    workCnt = 0
                    threadIndex += 1
                    threadWorker[threadIndex] = []
                workCnt += 1

        for i in threadWorker.keys():
            self.returnthreadWorker[i] = threadWorker[i][:10]
        return self.returnthreadWorker

    def updateProcess(self,urllist):
        for url in urllist :
            urlSplitLine = url.split("/")
            host = urlSplitLine[0]
            path = "/".join(urlSplitLine[1:len(urlSplitLine)])
            upQry = "update ListUrl set ProcessCondition = 1 where host = '"+host+"' and path ='/"+path+"'"
            updateDataHandler = queryOnTable.DBQuery()
            self.receiveData = updateDataHandler.updateQry(upQry)

    def doneProcess(self,url):
        urlSplitLine = url.split("/")
        host = urlSplitLine[0]
        path = "/".join(urlSplitLine[1:len(urlSplitLine)])
        upQry = "update ListUrl set ProcessCondition = 2 where host = '"+host+"' and path ='/"+path+"'"
        updateDataHandler = queryOnTable.DBQuery()
        self.receiveData = updateDataHandler.updateQry(upQry)

