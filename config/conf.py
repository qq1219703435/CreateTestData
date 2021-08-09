#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 创建者：赵承钰
# 修改时间：2019/12/06
# 配置文件的增删改查
import os.path
from configparser import ConfigParser
from logs import log
import traceback
log = log.Log()


class ConFig(object):
    # 获取ini
    def __init__(self, file_path=None):
        config = ConfigParser()
        self.config = config
        if file_path is None:
            self.file_path = os.path.abspath(os.path.dirname(__file__)) + "\\config.ini"
        else:
            self.file_path = file_path
        self.config.read(self.file_path, encoding='utf-8')

    # 获取数据
    # noinspection PyBroadException
    def conf_path(self, title, field=None):
        try:
            if field is None:
                return self.config.items(title)
            else:
                return self.config.get(title, field)
        except Exception:
            log.debug(traceback.format_exc())

    # 新增标题
    # noinspection PyBroadException
    # 上一段注释是为了，不显示Exception警告
    def conf_add(self, title):
        try:
            self.config.add_section(title)
            with open(self.file_path, "w") as f:
                self.config.write(f)
        except Exception:
            log.error(traceback.format_exc())

    # 修改数据，如果没有则新建
    # noinspection PyBroadException
    def conf_update(self, title, field, value):
        try:
            self.config.set(title, field, value)
            with open(self.file_path, "w", encoding='utf-8') as f:
                self.config.write(f)
        except Exception:
            log.error(traceback.format_exc())

    # 删除数据
    # noinspection PyBroadException
    def conf_delect(self, title, field):
        try:
            self.config.remove_option(title, field)
            with open(self.file_path, "w") as f:
                self.config.write(f)
        except Exception:
            log.error(traceback.format_exc())


if __name__ == '__main__':
    file = str("F:\\fireTree\\analysis_data\\analysis_config\\analysis_config.ini")
    a = ConFig(file).conf_path("oracle70")
    print(a)
