#!/usr/bin/python3
# -*- coding:utf-8 -*-

from config import conf
import cx_Oracle
import pandas as pd
import json
cof = conf.ConFig()


class ConnectDB(object):
    """初始化"""

    def __init__(self, user=None, password=None, ip=None, port=None, service_name=None,):
        """初始化参数"""
        self.user = user
        self.password = password
        self.ip = ip
        self.port = port
        self.service_name = service_name
        self.db = None
        self.cur = None

    def check_version(self):
        """查看oracle版本"""
        print(cx_Oracle.clientversion())

    def connect(self):
        """链接请求"""
        try:
            self.db = cx_Oracle.connect(str(self.user) + '/' + str(self.password) + '@' + str(self.ip) + ':' +
                                        str(self.port) + '/' + str(self.service_name))
            self.db.autocommit = False
            self.cur = self.db.cursor()
            return True
        except Exception as e:
            print("can't connect database!",e)
            return False

    def close_connect(self):
        """关闭光标及数据库链接"""
        self.cur.close()
        self.db.close()

    def go_sql(self, sql):
        """SQL部分"""
        self.sql = sql
        return self.sql

    # 插入数据
    def insert(self, sql_args):
        try:
            self.cur.executemany(self.sql, sql_args)
            return True
        except Exception as e:
            print(e)
            return False

    # 执行sql
    def execute(self):
        try:
            self.cur.execute(self.sql)
            return True
        except Exception as e:
            print(e)
            return False

    # 提交事务
    def commit(self):
        self.db.commit()

    # 返回数据
    def read_data(self, size=0):
        """触发输出结果"""
        data_list = ''
        if self.connect():
            if self.execute():
                if size:
                    data_list = self.cur.fetchmany(size)
                else:
                    data_list = self.cur.fetchall()
                return data_list
            self.close_connect()
        else:
            return False
        self.close_connect()


# panda列表
class DataToDF(ConnectDB):

    def __init__(self, user, password, ip, port, service_name):
        super().__init__(user, password, ip, port, service_name)

    def read_data(self, size=0):
        if self.connect():
            """输出格式定义"""
            if self.execute():
                if size:
                    data_list = self.cur.fetchmany(size)
                else:
                    data_list = self.cur.fetchall()
                columns = [i[0].lower() for i in self.cur.description]
                df = pd.DataFrame(data_list, columns=columns)
                self.close_connect()
                return df
        else:
            self.close_connect()
            return False


# 输出列表格式
class DataTolist(ConnectDB):
    def __init__(self, user, password, ip, port, service_name):
        super().__init__(user, password, ip, port, service_name)

    def lists(self, data):
        """转二维数组"""
        b = list(data)
        for c in b:
            b[b.index(c)] = list(c)
        return b

    def read_data(self, size=0):
        dl = []
        if self.connect():
            if self.execute():
                """输出格式定义"""
                if size:
                    data_list = self.cur.fetchmany(size)
                else:
                    data_list = self.cur.fetchall()
                dl = self.lists(data_list)
                self.close_connect()
                return dl
        else:
            self.close_connect()
            return False


# 输出字典格式
class DataTodict(ConnectDB):
    def __init__(self, user, password, ip, port, service_name):
        super().__init__(user, password, ip, port, service_name)

    def read_data(self, size=0):
        if self.connect():
            if self.execute():
                """输出格式定义"""
                if size:
                    data_list = self.cur.fetchmany(size)
                else:
                    data_list = self.cur.fetchall()
                col_name = self.cur.description
                if size == 1:
                    for row in data_list:
                        dict = {}
                        for col in range(len(col_name)):
                            key = col_name[col][0]
                            value = row[col]
                            dict[key] = value
                        return dict
                else:
                    list = []
                    for row in data_list:
                        dict = {}
                        for col in range(len(col_name)):
                            key = col_name[col][0]
                            value = row[col]
                            dict[key] = value
                        list.append(dict)
                    return list
                self.close_connect()
        else:
            self.close_connect()
            return False


if __name__ == '__main__':
    path = dict(cof.conf_path(title="oracle70"))
    user = path['user']
    password = path['password']
    ip = path['ip']
    port = path['port']
    service_name = path['service_name']
    db = ConnectDB(user,password,ip,port,service_name)
    connect = db.connect()
    sql = """UPDATE HDC_ADS.ADS_PATIENT_FINAL_ZHAO SET DRG_CODE = '1' WHERE pid = '170669208jflyq'"""
    db.go_sql(sql)
    db.execute()
    db.commit()

    # db.go_sql("SELECT * FROM agg_drgs_ratuinfo_fyfl WHERE PID = '2020521518510002'")
    # data = db.execute()
    # lists = db.read_data(1)
    # print(lists)
    # print(len(lists))

    # path136 = dict(cof.conf_path(title="oracle136"))
    # user136 = path136['user']
    # password136 = path136['password']
    # ip136 = path136['ip']
    # port136 = path136['port']
    # service_name136 = path136['service_name']
    # 链接数据库   我这边是把数据库的参数写到了配置文件里  直接填写也可以
    # user = "HDC_DWD"
    # password = "HDC_DWD_1Qaz"
    # ip = "172.16.3.70"
    # port = "1521"
    # service_name = "predb"
    # 先链接数据库, 分别是获取列表、字典、pandas的格式
    # db = DataTolist(user, password, ip, port, service_name)
    # db = DataTodict(user, password, ip, port, service_name)
    # db = DataToDF(user, password, ip, port, service_name)
    # 获取光标
    # connect136 = db.connect()
    # 编写SQL
    # size为获取条数，默认是0
    # db_data = db.read_data(size=5)
