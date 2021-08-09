import time
import config.conf
import random
import datetime
cof = config.conf.ConFig()


class UtilityClass(object):
    def __init__(self):
        pass

    # 获取当前时间戳
    def get_timestamp(self):
        millis = int(round(time.time() * 1000))
        return millis

    def get_time(self):
        millis = int(round(time.time()))
        return millis

    # 获取当前时间
    def get_new_time(self):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return now

    # 生成随机姓名
    def get_chinese(self):
        family_name = eval(cof.conf_path("name", "family_name"))
        given_name = eval(cof.conf_path("name", "given_name"))
        string_list = []
        family_name = random.choice(family_name)
        given_name = random.choice(given_name)
        string_list.append(family_name + given_name)
        chinese = "".join(string_list)
        return chinese

    # 生成随机身份证号
    def get_card(self):
        first_list = ['362402', '362421', '362422', '362423', '362424', '362425', '362426', '362427', '362428',
                      '362429', '362430', '362432', '110100', '110101', '110102', '110103', '110104', '110105',
                      '110106', '110107', '110108', '110109', '110111', '411503']
        first = random.choice(first_list)
        now = time.strftime('%Y')
        # 1948为第一代身份证执行年份,now-18直接过滤掉小于18岁出生的年份
        second = random.randint(1948,int(now)-18)
        age = int(now) - second
        # print('随机生成的身份证人员年龄为：'+str(age))
        three = random.randint(1,12)
        # 月份小于10以下，前面加上0填充
        if three < 10:
            three = '0' + str(three)
        four = random.randint(1,31)
        # 日期小于10以下，前面加上0填充
        if four < 10:
            four = '0' + str(four)
        five = random.randint(1,9999)
        if five < 10:
            five = '000' + str(five)
        elif 10 < five < 100:
            five = '00' + str(five)
        elif 100 < five < 1000:
            five = '0' + str(five)
        id_card = str(first)+str(second)+str(three)+str(four)+str(five)
        return id_card


if __name__ == '__main__':
    a = UtilityClass().get_chinese()
    b = UtilityClass().get_card()
    print(a, b)
