# _*_ coding: utf-8 _*_
# Create your views here.
# monitor control

from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Template, Context
import datetime
import hashlib
from databaseinfo import queryOnTable, confTableAttr


def SelectData(queryIn):
    enumCondition = {'0':'수집대상','1':'수집진행중','2':'수집완료'}
    sqlHandle = queryOnTable.DBQuery()
    tblConf = confTableAttr.confAttr()

    try :
        urlSplitLine = queryIn.split("/")
        host = urlSplitLine[0]
        path = "/"+"/".join(urlSplitLine[1:len(urlSplitLine)])
    except Exception, e:
        return "ERROR"

    infoUrl = host + path
    tableIndex = long(hashlib.md5(infoUrl).hexdigest(), 16) % 2
    orderedQry = "select ListURL.host, ListURL.path, ListURL.extractdate, ListURL.processcondition, \
                 Body.title, Body.body, Body.createdate, Body.statuscode from ListURL, Body_"+str(tableIndex)+" as Body where  \
                 ListURL.host='"+host+"' and ListURL.path = '"+path+"' and Body.host='"+host+"' and Body.path = '"+path+"' "
    receiveData = sqlHandle.selectQry(orderedQry)
    try :
        reHost = receiveData[0]['host']
    except Exception, e:
        return "ERROR"
    rePath = receiveData[0]['path']
    reProcessCondition = receiveData[0]['processcondition']
    reExtractDate = receiveData[0]['extractdate']
    reTitle = receiveData[0]['title']
    reBody = "\n" + receiveData[0]['body'].replace(".", ".\n")
    reCreateDate = receiveData[0]['createdate']
    reStatusCode = receiveData[0]['statuscode']
    sqlHandle.close()
    resultOut =             "<PRE><P>"
    resultOut = resultOut + "</P><P><STRONG>URL               >> </STRONG><A href='" + "http://" + reHost + rePath +"' " \
                            "target='blank'>http://" + reHost + rePath + "</A>"
    resultOut = resultOut + "</P><P><STRONG>Process Condition >> </STRONG>" + enumCondition[str(reProcessCondition)]
    resultOut = resultOut + "</P><P><STRONG>Extract Date      >> </STRONG>" + str(reExtractDate)
    resultOut = resultOut + "</P><P><STRONG>Status Code       >> </STRONG>" + str(reStatusCode)
    resultOut = resultOut + "</P><P><STRONG>News Create Date  >> </STRONG>" + str(reCreateDate)
    resultOut = resultOut + "</P><P><STRONG>Title             >> </STRONG>" + str(reTitle)
    resultOut = resultOut + "</P><P><STRONG>BODY Text         >> </STRONG>" + str(reBody)
    resultOut = resultOut + "</P></PRE>"
    return resultOut

# index.html 을 지정 파라미터는  {{ head_title }}, {{ page_title }} 에 '한글'
def index(request):
    return render_to_response('index.html',)

def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_datetime':now})

def search_form(request):
    return render_to_response('notice.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        questionIn = request.GET['q']
        message = SelectData(questionIn)
        if message == "ERROR":
            return render_to_response('notice.html', {'error':True})
        else:
            #print message
            return HttpResponse(message)
    else:
        return render_to_response('notice.html', {'error': True})


