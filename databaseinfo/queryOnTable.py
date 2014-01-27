# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors
import sys,os
sys.path.append(os.path.dirname(os.path.abspath('../pseudo_crawler')))
from pseudo_crawler import settings

def dictValuePad(key):
    return '%(' + str(key) + ')s'

# use this control command
class DBQuery(object) :
    def __init__(self):
        self.db = MySQLdb.connect(host=settings.DATABASES['default']['HOST'], user=settings.DATABASES['default']['USER'], passwd=settings.DATABASES['default']['PASSWORD'], db=settings.DATABASES['default']['NAME'],cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.db.cursor()
        self.cursor.execute("set names utf8")

    def executeQry(self, Query):
        self.cursor.execute(Query)
        self.db.commit()

    def executeMapQry(self, Query, dict):
        self.cursor.execute(Query, dict)
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()

    def closeQry(self):
        self.cursor.close()
        self.db.close()

    def dictValuePad(key):
        return '%(' + str(key) + ')s'

    def makeInsertQry(self, table, dict):
        sql = 'INSERT INTO ' + table
        sql += ' ('
        sql += ', '.join(dict)
        sql += ') VALUES ('
        sql += ', '.join(map(dictValuePad, dict))
        sql += ');'
        return sql

    def selectQry(self, Query):
        self.cursor.execute(Query)
        self.records = self.cursor.fetchall()
        return self.records

    def updateQry(self, Query):
        self.cursor.execute(Query)
        self.db.commit()

