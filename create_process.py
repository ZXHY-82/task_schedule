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


def tasks_create(pid, _time, task):
    level = task[0]
    cpu = task[1]
    mem = task[2]
    create_time = _time
    last_time = task[3]
    a = [pid, level, cpu, mem, create_time, last_time, "0000/00/00 00:00:00", "0000/00/00 00:00:00", 0]
    return a



if __name__ == '__main__':
    nums = []
    tasks = [] # [level, cpu, mem, last_time]
    sleep_time = []
    i = 0
    while i < 300:
        num = random.randint(2, 6)
        nums.append(num)
        sleep = random.randint(1, 2)
        sleep_time.append(sleep)
        for j in range(num):
            cpu = random.randint(5, 25)
            mem = random.randint(5, 25)
            temp = [random.randint(1, 3), cpu,
                    mem, random.randint(int((cpu + mem)/5), int((cpu + mem)/2))]
            tasks.append(temp)
            i = i + 1
    print(nums)
    print(sleep_time)
    print(tasks)
"""
nums = [6, 4, 2, 6, 6, 1, 4, 1, 4, 5, 2, 2, 3, 6, 1, 1, 2, 1, 3, 5, 3, 6, 1, 3, 4, 6, 5, 1, 1, 1, 3, 5, 4, 2, 5, 5, 6, 5, 3, 2, 3, 4, 1, 6]
sleep_time = [2, 3, 2, 1, 2, 1, 1, 2, 1, 3, 1, 3, 1, 1, 2, 1, 1, 1, 3, 2, 3, 3, 2, 3, 2, 2, 1, 2, 3, 2, 3, 3, 3, 3, 2, 2, 2, 1, 3, 2, 2, 3, 2, 1]
tasks = [[1, 4, 4, 2], [1, 5, 5, 3], [3, 5, 4, 4], [2, 3, 2, 3], [3, 4, 1, 3], [1, 4, 2, 3], [2, 1, 5, 7], [2, 4, 4, 4], [2, 2, 4, 4], [2, 1, 4, 1], [2, 2, 3, 3], [3, 2, 3, 10], [3, 2, 4, 8], [2, 2, 2, 9], [3, 4, 4, 4], [1, 5, 2, 3], [2, 5, 5, 9], [2, 1, 2, 5], [2, 2, 5, 8], [3, 3, 3, 7], [1, 2, 5, 5], [3, 4, 4, 4], [2, 1, 3, 2], [2, 5, 4, 1], [3, 2, 3, 1], [3, 3, 1, 1], [3, 4, 3, 7], [2, 1, 4, 9], [1, 4, 4, 5], [2, 5, 1, 8], [3, 2, 5, 5], [3, 3, 5, 9], [2, 3, 3, 7], [3, 3, 4, 6], [1, 1, 1, 8], [3, 1, 3, 10], [1, 5, 5, 7], [3, 3, 5, 6], [3, 1, 2, 1], [3, 4, 2, 10], [1, 3, 3, 1], [2, 2, 4, 9], [2, 3, 3, 4], [2, 3, 5, 7], [2, 5, 1, 4], [1, 1, 1, 3], [1, 1, 5, 1], [3, 3, 3, 6], [2, 4, 1, 9], [1, 3, 2, 2], [1, 5, 3, 5], [1, 1, 2, 4], [1, 1, 4, 5], [1, 2, 2, 3], [2, 3, 4, 2], [2, 3, 2, 3], [3, 4, 4, 4], [1, 2, 1, 10], [2, 3, 3, 9], [1, 4, 3, 5], [2, 1, 4, 2], [3, 3, 3, 8], [2, 3, 2, 9], [3, 5, 5, 9], [2, 2, 3, 8], [2, 2, 1, 9], [3, 2, 3, 7], [1, 2, 5, 6], [1, 3, 3, 5], [1, 1, 4, 10], [3, 2, 4, 4], [3, 3, 5, 4], [1, 3, 4, 8], [1, 3, 2, 2], [3, 4, 3, 3], [2, 4, 1, 10], [1, 3, 3, 5], [3, 2, 4, 9], [3, 3, 4, 3], [1, 3, 3, 3], [2, 5, 2, 9], [2, 5, 3, 8], [2, 3, 5, 2], [1, 3, 1, 9], [1, 2, 3, 8], [3, 5, 4, 2], [3, 2, 5, 6], [1, 1, 5, 4], [3, 5, 2, 4], [1, 3, 3, 2], [3, 5, 5, 5], [2, 5, 3, 1], [3, 5, 2, 6], [3, 5, 2, 2], [2, 4, 4, 1], [2, 4, 5, 9], [1, 5, 1, 8], [1, 2, 5, 8], [3, 4, 3, 1], [1, 4, 2, 6], [3, 4, 3, 7], [1, 1, 5, 4], [3, 1, 3, 9], [1, 3, 1, 7], [3, 5, 5, 1], [2, 5, 1, 3], [3, 4, 3, 5], [2, 4, 1, 9], [1, 2, 5, 10], [2, 1, 2, 10], [2, 4, 4, 9], [3, 2, 2, 1], [2, 5, 4, 7], [1, 1, 4, 8], [1, 5, 3, 4], [1, 5, 4, 2], [3, 4, 3, 7], [2, 4, 3, 3], [3, 5, 4, 1], [3, 5, 4, 9], [3, 2, 4, 3], [1, 3, 2, 2], [1, 3, 3, 2], [1, 5, 4, 5], [2, 5, 1, 5], [1, 4, 5, 2], [2, 4, 5, 10], [3, 4, 2, 8], [3, 1, 3, 5], [1, 2, 5, 8], [3, 2, 2, 7], [1, 1, 1, 5], [3, 3, 4, 3], [3, 4, 3, 7], [3, 1, 1, 7], [1, 5, 3, 6], [2, 4, 1, 2], [2, 2, 3, 9], [2, 2, 1, 9], [3, 2, 4, 10], [2, 3, 4, 1], [2, 5, 4, 8], [3, 4, 2, 4], [1, 3, 2, 5], [3, 2, 3, 8], [1, 3, 2, 1], [3, 4, 1, 8], [2, 4, 1, 9], [2, 2, 1, 9], [3, 1, 4, 8]]
nums = [3, 2, 4, 4, 3, 2, 4, 5, 3, 5, 5, 5, 6, 6, 6, 2, 2, 3, 4, 5, 5, 5, 2, 5, 3, 3, 6, 5, 2, 2, 4, 3, 2, 4, 3, 4, 4, 2, 6, 4]
sleep_time = [2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1]
tasks = [[3, 19, 20, 14], [1, 21, 5, 13], [2, 21, 8, 14], [1, 24, 6, 7], [2, 25, 22, 18], [3, 18, 24, 15], [1, 8, 18, 8], [2, 7, 13, 4], [1, 14, 19, 8], [3, 5, 11, 8], [3, 6, 11, 8], [3, 24, 11, 7], [1, 15, 15, 15], [3, 17, 6, 9], [2, 18, 13, 7], [3, 16, 22, 18], [2, 22, 19, 10], [3, 12, 15, 10], [3, 11, 7, 7], [3, 21, 24, 11], [1, 15, 18, 15], [3, 22, 10, 14], [1, 23, 21, 16], [1, 12, 21, 9], [2, 15, 25, 17], [3, 19, 13, 15], [2, 9, 19, 5], [3, 9, 7, 3], [1, 11, 24, 10], [1, 10, 25, 16], [2, 10, 12, 9], [3, 11, 9, 6], [1, 18, 19, 16], [1, 25, 13, 15], [3, 5, 10, 5], [2, 18, 16, 11], [3, 8, 25, 15], [2, 21, 18, 10], [3, 21, 13, 10], [1, 9, 12, 10], [3, 14, 18, 9], [2, 13, 15, 13], [3, 19, 9, 6], [2, 21, 18, 8], [1, 25, 8, 10], [2, 8, 6, 7], [3, 7, 20, 6], [1, 12, 16, 12], [3, 20, 5, 9], [3, 5, 10, 7], [2, 21, 15, 10], [2, 22, 14, 17], [1, 19, 19, 16], [1, 14, 21, 16], [3, 24, 9, 11], [2, 16, 25, 15], [2, 25, 12, 7], [3, 14, 21, 8], [2, 12, 21, 8], [2, 22, 19, 11], [2, 16, 9, 7], [3, 20, 19, 18], [2, 15, 14, 12], [3, 14, 9, 10], [2, 8, 8, 8], [1, 19, 24, 15], [3, 7, 22, 8], [2, 11, 10, 5], [1, 8, 9, 4], [3, 24, 24, 12], [1, 19, 22, 20], [3, 22, 19, 20], [1, 25, 13, 14], [3, 18, 6, 4], [3, 7, 17, 9], [1, 8, 18, 13], [3, 11, 13, 8], [2, 13, 12, 6], [2, 11, 15, 8], [2, 7, 18, 5], [1, 20, 24, 16], [2, 12, 22, 13], [1, 5, 21, 11], [1, 16, 5, 4], [1, 17, 20, 13], [1, 20, 25, 10], [2, 20, 17, 11], [3, 9, 21, 14], [3, 22, 22, 18], [2, 21, 22, 20], [2, 23, 13, 7], [1, 24, 8, 11], [2, 17, 6, 11], [2, 7, 7, 4], [1, 13, 22, 9], [2, 21, 18, 11], [2, 19, 6, 8], [1, 16, 24, 14], [3, 23, 16, 19], [1, 9, 22, 12], [1, 18, 7, 10], [2, 15, 23, 12], [2, 7, 8, 7], [3, 22, 20, 15], [1, 9, 9, 9], [3, 10, 15, 5], [1, 8, 13, 8], [1, 13, 16, 11], [1, 20, 22, 15], [1, 22, 23, 19], [3, 17, 19, 8], [2, 7, 21, 7], [3, 24, 23, 15], [3, 13, 13, 11], [1, 24, 8, 13], [2, 20, 9, 9], [3, 15, 21, 16], [2, 13, 8, 6], [3, 25, 14, 18], [1, 14, 6, 4], [3, 5, 13, 9], [1, 17, 9, 12], [2, 19, 11, 6], [3, 14, 21, 17], [2, 23, 19, 14], [1, 8, 13, 10], [2, 17, 23, 9], [3, 15, 8, 4], [2, 9, 21, 11], [1, 23, 24, 9], [2, 24, 25, 17], [3, 8, 15, 4], [1, 16, 20, 18], [3, 9, 12, 5], [2, 13, 15, 6], [3, 17, 21, 12], [2, 9, 17, 12], [1, 19, 15, 15], [1, 19, 10, 11], [1, 23, 21, 8], [1, 5, 18, 7], [3, 12, 16, 11], [1, 19, 8, 5], [1, 5, 16, 4], [1, 17, 5, 10], [2, 17, 15, 6], [2, 14, 20, 17], [3, 20, 9, 7], [1, 7, 16, 9], [2, 6, 19, 5], [3, 25, 7, 10], [1, 7, 14, 4], [2, 19, 14, 9]]
"""