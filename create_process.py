import random

"""
process:[pid,level(1~3级),cpu,mem,create_time,last_time,run_time(初始为0),finish_time(初始为0),部署到的结点(初始为0)]
"""


def process_create(pid, _time):
    level = random.randint(1, 3)
    cpu = random.randint(1, 5)
    mem = random.randint(1, 5)
    create_time = _time
    last_time = random.randint(1, 10)
    a = [pid, level, cpu, mem, create_time, last_time, "0000/00/00 00:00:00", "0000/00/00 00:00:00", 0]
    return a
