# -*- coding: utf-8 -*-
# version: 0.1
import datetime
import time
from io import IOBase
from . import write_log_conf
import types
import traceback

class GetDateTime():
    def __init__(self):
        # 定义日期格式
        self.date_day_format_str = "%Y-%m-%d"
        self.date_sec_format_str = "%Y-%m-%d  %H:%M:%S"

    def get_cur_date_day(self):
        now = datetime.datetime.now()
        return now.strftime(self.date_day_format_str)
    def get_cur_date_sec(self):
        now = datetime.datetime.now()
        return now.strftime(self.date_sec_format_str)
    def get_cur_unix_sec(self):
        return int(time.time())


class WriteLog():
    def __init__(self, f, log_level):
        self.log_level_info = write_log_conf.log_level_info
        self.log_level_notice = write_log_conf.log_level_notice
        self.log_level_warn = write_log_conf.log_level_warn
        self.log_level_error = write_log_conf.log_level_error
        self.log_all_level = [self.log_level_info, self.log_level_notice, self.log_level_warn, self.log_level_error]

        self.get_date_time = GetDateTime()
        if log_level in self.log_all_level:
            self.log_level = log_level
        else:
            print("Error! \"%s\" is not one of %s" %(log_level, str(self.log_all_level) ))
            print("%s won't work" %(WriteLog.__name__))
        if isinstance(f, IOBase):
            if f.mode == 'a':
                self.f = f
            else:
                print("Error! \"%s\" should be add mode")
        else:
            print("Error! \"%s\" should be a file instance" %(str(f) ))
            print("%s won't work" % (WriteLog.__name__))


    def write_file(self, log_level_para, log_msg):
        """
        写入日志, 日志内容包含日期
        """
        # 日志告警级别不是定义的，则不记录日志
        if log_level_para not in self.log_all_level:
            return False
        # 大于告警级别的，则记录日志
        elif self.log_all_level.index(log_level_para) >= self.log_all_level.index(self.log_level):
            cur_date = self.get_date_time.get_cur_date_sec()
            name_invoke = traceback.extract_stack()[-2][2]
            log_info = "%s  %s  From %s  %s\n" %(cur_date, log_level_para, name_invoke, log_msg)
            try:
                self.f.write(log_info)
                self.f.flush()
            except Exception as e:
                print(e)


def mylog(when, file):
    def log(func, *args, **kwargs):
        log_level = write_log_conf.log_level_notice
        wlog = WriteLog(file, log_level)
        wlog.write_file(write_log_conf.log_level_notice, "called: %s" % func)

    def pre_logged(f):
        def wrapper(*args, **kwargs):
            log(f, *args, **kwargs)
            return f(*args, **kwargs)
        return wrapper

    def post_logged(f):
        if isinstance(f, types.FunctionType):
            def wrapper_func(*args, **kwargs):
                try:
                    return f(*args, **kwargs)
                finally:
                    log(f.__name__)
            return wrapper_func
        else:
            class_name = f.__name__
            orig_attr = f.__getattribute__

            def wrapper_cls(self, name, *args, **kwargs):
                method_name = "%s().%s" %(class_name, name)
                try:
                    return orig_attr(self, name, *args, **kwargs)
                finally:
                    log(method_name)
            f.__getattribute__ = wrapper_cls
            return f

    try:
        func = {"pre": pre_logged, "post": post_logged}[when]
        return func
    except KeyError as e:
        print(e)
        print("must be 'pre' or 'post'")










