# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import mysql.connector
import pymysql
import pymongo
from scrapy.conf import settings

class XiciToMysqlPipeline(object):

    def process_item(self, item, spider):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWD']
        db = settings['MYSQL_DBNAME']
        c = settings['CHARSET']
        port = settings['MYSQL_PORT']
        con = pymysql.connect(host=host,user=user,passwd=psd,db=db,charset=c,port=port)
        cur = con.cursor()
        print("mysql连接成功")
        sql = """insert into xicidaili(IP,PORT,ADDRESS,SPEED,LAST_CHECK_TIME)
        values(%s,%s,%s,%s,%s)"""
        lis = (item['IP'], item['PORT'], item['ADDRESS'], item['SPEED'],item['LAST_CHECK_TIME'])
        # # print(lis)
        try:
            cur.execute(sql,lis)
            print('写入数据库成功')
        except Exception as e:
            print("写入失败")

            con.rollback()
        else:
            con.commit()

        cur.close()
        con.close()

        return item

class XiciToJsonPipeline(object):
    def __init__(self):
        self.filename = open("xicidaili.json", "wb")

    def process_item(self, pre_item, spider):
        jsontext = json.dumps(dict(pre_item), ensure_ascii=False) + ",\n"
        self.filename.write(jsontext.encode("utf-8"))
        print('写入Json成功')
        return pre_item

    def close_spider(self, spider):
        self.filename.close()

class XiciToMongoPipeline(object):
    def __init__(self):
        port = settings['MONGODB_PORT']
        host = settings['MONGODB_HOST']
        db_name = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        ip = dict(item)
        self.post.insert(ip)
        print('写入Mongodb成功')
        return item