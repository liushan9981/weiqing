# -*- coding: utf-8 -*-
import traceback

from feijiang.writelog.write_log import WriteLog
from feijiang.writelog.write_log import mylog
from feijiang.writelog import write_log_conf

# 以下语句必须放在顶级
logpath = "/Users/bach.liu/mylab/weiqing/debug.log"
log_level = "INFO"
f = open(logpath, 'a')
wlog = WriteLog(f, log_level)


@mylog("post", f)
def test():
    # 打印日志
    wlog.write_file(write_log_conf.log_level_notice, "liushan")


class Test:
    def __init__(self):
        self.name = "liushan"

    # 装饰单个方法
    @mylog("post", f)
    def hello(self, name):
        print("1234 %s" % name)

    def haha(self):
        print("hhhh")
        print("this is haha: %s" % traceback.extract_stack()[-2][2])


# 装饰实例的所有方法
@mylog("pre", f)
class Test2:
    def __init__(self):
        self.name = 'test2'

    def func1(self):
        print("this is func1", self.name)
        wlog.write_file(write_log_conf.log_level_error, "func1 output")


# 装饰函数
@mylog("post", f)
def getname():
    mytest = Test()
    mytest.hello("shanshan")
    mytest.haha()
    mytest2 = Test2()
    mytest2.func1()


if __name__ == '__main__':
    getname()
    test()


