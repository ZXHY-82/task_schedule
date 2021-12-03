import random
import time
from lock import check_lock, file_lock, file_unlock
from create_process import process_create
from time_model import get_now_str, get_time_bystr, get_timedelta_bystr, begin_time


pid = 1
process_pool_1 = []  # 进程池level_1
process_pool_2 = []  # 进程池level_2
process_pool_3 = []  # 进程池level_3


def switch_level(level, pool_1, pool_2, pool_3, process):
    if level == 1:
        pool_1.append(process)
        """
        try:
            with open('pool_1.json', 'a+', encoding='utf-8') as fs:
                json.dump(process, fs)
        except IOError as e:
            print(e)
        """
        while check_lock("pool_1.txt", "pool_1_lock.txt"):
            time.sleep(0.05)
        file_lock("pool_1.txt", "pool_1_lock.txt")

        f = open("pool_1.txt", "a")
        for line in process:
            f.write(str(line) + ' ')
        f.write('\n')
        f.close()

        file_unlock("pool_1.txt", "pool_1_lock.txt")

        return pool_1
    elif level == 2:
        pool_2.append(process)
        """
        try:
            with open('pool_1.json', 'a+', encoding='utf-8') as fs:
                json.dump(process, fs)
        except IOError as e:
            print(e)
        """
        while check_lock("pool_2.txt", "pool_2_lock.txt"):
            time.sleep(0.05)
        file_lock("pool_2.txt", "pool_2_lock.txt")

        f = open("pool_2.txt", "a")
        for line in process:
            f.write(str(line) + ' ')
        f.write('\n')
        f.close()

        file_unlock("pool_2.txt", "pool_2_lock.txt")

        return pool_2
    elif level == 3:
        pool_3.append(process)
        """"
        try:
            with open('pool_1.json', 'a+', encoding='utf-8') as fs:
                json.dump(process, fs)
        except IOError as e:
            print(e)
        """
        while check_lock("pool_3.txt", "pool_3_lock.txt"):
            time.sleep(0.05)
        file_lock("pool_3.txt", "pool_3_lock.txt")

        f = open("pool_3.txt", "a")
        for line in process:
            f.write(str(line) + ' ')
        f.write('\n')
        f.close()

        file_unlock("pool_3.txt", "pool_3_lock.txt")
        return pool_3


# begin_time = get_now_str()
# current_time = 0
# 创建20个进程并加入进程池
i = 20
while i > 0:
# while 1:
    sleep = random.randint(1, 5)  # 随机等待一段时间
    for j in range(sleep):
        time.sleep(1)
    # temp = process_create(pid, current_time)  # 创建一个进程
    # temp = process_create(pid, get_timedelta_bystr(begin_time, get_now_str()))
    temp = process_create(pid, get_now_str())
    switch_level(temp[1], process_pool_1, process_pool_2, process_pool_3, temp)  # 放入对应进程池
    print("生成任务"+str(pid)+"成功")
    i -= 1
    pid += 1
