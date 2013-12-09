#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys, os
import urllib2
import time
from time import gmtime, strftime
sys.path.append(os.path.dirname(os.path.abspath('../databaseinfo')))
from parser import extractLink
from databaseinfo import queryOnTable, confTableAttr
from handleprocess import controlJob

sqlHandle = queryOnTable.DBQuery()
tblConf = confTableAttr.confAttr()
pointJob = controlJob.ControlPoint()

gTodayInfo = time.strftime("%Y%m%d", gmtime())
seedUrlList = {'DAUM': "http://sports.media.daum.net/worldbaseball/news/breaking/list.html?cateid=1015&regdate="+gTodayInfo+"&page=",
               'NAVER':"http://sports.news.naver.com/sports/index.nhn?category=worldbaseball&ctg=news&mod=lst&type=news&date="+gTodayInfo+"&page="}
prefixHostUrl = {'DAUM':"sports.media.daum.net",'NAVER':"sports.news.naver.com"}
prefixPathUrl = {'DAUM':"/worldbaseball/news/breaking/", 'NAVER':"/sports/index.nhn?category=worldbaseball&ctg=news&mod=read&office_id="}
validListUrl = {'DAUM':"view.html?cateid=1015", 'NAVER':"/sports/index.nhn?category=worldbaseball&ctg=news&mod=read&office_id="}
returnNewTotalLink = {'DAUM':[], 'NAVER':[]}

for siteName in seedUrlList.keys():
    nCheckCnt = 0
    nPageIdx = 1
    bLook = True
    while bLook == True:
        # URL 수집 후 해당 데이터를 기록
        response = None
        curlUrl = seedUrlList[siteName] + str(nPageIdx)
        print curlUrl
        req = urllib2.Request(curlUrl)
        try :
            response = urllib2.urlopen(req).read()
        except urllib2.URLError as e:
            #print e.reason
            pass
        except urllib2.HTTPError as e:
            #print e.code
            pass

        extractLinkInfo = extractLink(response)
        for extractNumberInfo in extractLinkInfo:
            if validListUrl[siteName] in str(extractNumberInfo.get('href')):
                if validListUrl[siteName] == prefixPathUrl[siteName] :
                    if str(extractNumberInfo.get('href'))[0] == '/':
                        pathURL = str(extractNumberInfo.get('href'))
                    else:
                        continue
                else:
                    pathURL = prefixPathUrl[siteName] + str(extractNumberInfo.get('href'))
                if pathURL in returnNewTotalLink[siteName]:
                    continue
                else:
                    returnNewTotalLink[siteName].append(pathURL)

        bLook = pointJob.noCountData(returnNewTotalLink[siteName])

        for pathDetailURL in returnNewTotalLink[siteName]:
            mapURLAttrs = tblConf.URLAttrs
            mapURLAttrs['Host'] = prefixHostUrl[siteName]
            mapURLAttrs['Path'] = pathDetailURL
            mapURLAttrs['ProcessCondition'] = 0
            mapURLAttrs['Priority'] = 0
            mapURLAttrs['ExtractDate'] = tblConf.nowTime()
            mapURLAttrs['ExtractEndDate'] = 0
            mapURLAttrs['InversedDate'] = tblConf.inverseTime(mapURLAttrs['ExtractDate'])
            sInsertQry = sqlHandle.makeInsertQry("ListURL", mapURLAttrs)
            try :
                sqlHandle.executeMapQry(sInsertQry, mapURLAttrs)
            except Exception, e:
                if "Duplicate entry" in str(e):
                    nCheckCnt += 1
                bLook = pointJob.breakPoint(siteName,nCheckCnt)
                if bLook == False:
                    break
        returnNewTotalLink[siteName] = []
        nPageIdx += 1
        pointJob.sleepPoint(siteName)
