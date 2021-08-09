#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 创建者：赵承钰
# 修改时间：2019/12/06
# 封装日志模块
import logging
import time
import os


class Log(object):

    def __init__(self):
        # log_path是存放日志的路径
        file_path = os.path.abspath(os.path.dirname(__file__))
        current_time = time.strftime("%Y_%m_%d", time.localtime(time.time()))
        pic_path = file_path + '\\' + current_time + '\\'
        # 如果不存在这个log文件夹，就自动创建一个 os.getcwd()
        if not os.path.exists(pic_path):
            os.mkdir(pic_path)
        # 文件的命名
        name = pic_path + time.strftime('%Y_%m_%d') + '.log'
        self.logname = os.path.join(name)
        self.logger = logging.getLogger(pic_path)
        logging.basicConfig()
        self.logger = logging.getLogger("mylogger")
        # 设置日志级别
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(pathname)s\
- %(levelname)s: %(message)s')

    def __console(self, level, msg):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')  # 这个是python3的
        self.logger.addHandler(fh)
        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(msg)
        elif level == 'debug':
            self.logger.debug(msg)
        elif level == 'warning':
            self.logger.warning(msg)
        elif level == 'error':
            self.logger.error(msg)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()

    def debug(self, msg):
        self.__console('debug', msg)

    def info(self, msg):
        self.__console('info', msg)

    def warning(self, msg):
        self.__console('warning', msg)

    def error(self, msg):
        self.__console('error', msg)


if __name__ == '__main__':
    Log().info(msg="hhahahahha")

"""
logging.basicConfig函数各参数：
filename：指定日志文件名；
filemode：和file函数意义相同，指定日志文件的打开模式，'w'或者'a'；
format：指定输出的格式和内容，format可以输出很多有用的信息，
参数：作用
%(levelno)s：打印日志级别的数值
%(levelname)s：打印日志级别的名称
%(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s：打印当前执行程序名
%(funcName)s：打印日志的当前函数
%(lineno)d：打印日志的当前行号
%(asctime)s：打印日志的时间
%(thread)d：打印线程ID
%(threadName)s：打印线程名称
%(process)d：打印进程ID
%(message)s：打印日志信息
datefmt：指定时间格式，同time.strftime()；
level：设置日志级别，默认为logging.WARNNING；
stream：指定将日志的输出流，可以指定输出到sys.stderr，sys.stdout或者文件，默认输出到sys.stderr，当stream和filename同时指定时，
stream被忽略；
traceback.print_exc()跟traceback.format_exc()有什么区别呢？
format_exc()返回字符串，print_exc()则直接给打印出来。
"""
