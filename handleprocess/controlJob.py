# -*- coding:utf-8 -*-

# This is for taget with DB control
import time
import md5

class ControlPoint():

    def __init__(self):
        self.threadCnt = 4

    def sleepPoint(self, siteName):
        if "daum" in siteName or "DAUM" in siteName:
            siteName = "DAUM"
        else:
            siteName = "NAVER"
        self.sleepTime = {'DAUM': 1, 'NAVER': 2}
        time.sleep(self.sleepTime[siteName])

    def breakPoint(self, siteName, currentCnt):
        if "daum" in siteName or "DAUM" in siteName:
            siteName = "DAUM"
        else:
            siteName = "NAVER"
        self.breakTime = {'DAUM': 5, 'NAVER': 5}
        if currentCnt > self.breakTime[siteName]:
            return False
        else:
            return True

    def noCountData(self, currentList):
        if len(currentList) == 0:
            return False
        else:
            return True

