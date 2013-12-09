# -*- coding: utf-8 -*-

import MySQLdb
import sys,os
sys.path.append(os.path.dirname(os.path.abspath('../pseudo_crawler')))
from pseudo_crawler import settings

db = MySQLdb.connect(host=settings.DATABASES['default']['HOST'], user=settings.DATABASES['default']['USER'], passwd=settings.DATABASES['default']['PASSWORD'], db=settings.DATABASES['default']['NAME'])
cursor = db.cursor()
cursor.execute("set names utf8")

def createTableBody(tableName):
    return  """CREATE TABLE """ +tableName+ """ (
            `Host` varchar(32) COLLATE utf8_bin NOT NULL,
            `Path` varchar(128) COLLATE utf8_bin DEFAULT NULL,
            `title` mediumtext COLLATE utf8_bin DEFAULT NULL,
            `Body`  text COLLATE utf8_bin DEFAULT NULL,
            `StatusCode` int(4) COLLATE utf8_bin DEFAULT 0,
            `ExtractDate` datetime COLLATE utf8_bin,
            `CreateDate` datetime COLLATE utf8_bin,
            `InversedDate` int(11) COLLATE utf8_bin,
            PRIMARY KEY `URL` (`Host`,`Path`),
            KEY `InversedDate`  (`InversedDate`),
            KEY `StatusCode` (`StatusCode`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"""

def createTableList(tableName):
    return  """CREATE TABLE """ +tableName+ """ (
            `Host` varchar(32) COLLATE utf8_bin NOT NULL,
            `Path` varchar(128) COLLATE utf8_bin DEFAULT NULL,
            `ProcessCondition` tinyint(1) COLLATE utf8_bin DEFAULT 0,
            `Priority` tinyint(1) COLLATE utf8_bin DEFAULT 0,
            `ExtractDate` datetime COLLATE utf8_bin,
            `ExtractEndDate` datetime COLLATE utf8_bin,
            `InversedDate` int(11) COLLATE utf8_bin,
            PRIMARY KEY `URL` (`Host`,`Path`),
            KEY `InversedDate`  (`InversedDate`),
            KEY `Priority` (`Priority`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin"""

try:
    cursor.execute(createTableList("listURL"))
except Exception, e:
    cursor.execute("DROP TABLE ListURL")
    cursor.execute(createTableList("listURL"))

bodytableList = ["Body_0", "Body_1"]
for tableName in bodytableList:
    try:
        cursor.execute(createTableBody(tableName))
    except Exception, e:
        cursor.execute("DROP TABLE " + tableName)
        cursor.execute(createTableBody(tableName))
cursor.close()
db.commit()
db.close()
