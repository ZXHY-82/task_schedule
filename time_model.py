import datetime

format = "%Y/%m/%d %H:%M:%S"


# 获取现在时间的字符串
def get_now_str():
    a = datetime.datetime.now()
    a = a.strftime(format)
    return a


# 将字符串转为时间
def get_time_bystr(str):
    mt = datetime.datetime.strptime(str, format)
    return mt


# 返回两时间的差
def get_timedelta_bystr(time1, time2):
    return (get_time_bystr(time2) - get_time_bystr(time1)).seconds


def get_time_finish(time1, seconds):
    a = (get_time_bystr(time1) + datetime.timedelta(seconds=seconds))
    a = a.strftime(format)
    return a


begin_time = get_now_str()
