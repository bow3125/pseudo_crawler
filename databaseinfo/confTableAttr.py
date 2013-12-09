import time
from time import gmtime, strftime

class confAttr :
    def __init__(self):
        self.URLAttrs = {'Host':"",'Path': "",'ProcessCondition': "",'Priority': "",'ExtractDate': "",'ExtractEndDate': "",'InversedDate': ""}
        self.BODYAttrs = {'Host':"",'Path':"",'Title':"",'Body':"",'StatusCode':"",'ExtractDate':"","CreateDate":"","InversedDate":""}

    def inverseTime(self,datetime):
        datetime = datetime[2:len(datetime)-2]
        inveredDateTime = "-" + str(datetime).replace("-", "").replace(":", "").replace(".","").replace(" ", "")
        return inveredDateTime

    def nowTime(self):
        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return nowTime

