import random
import time
import os
from time_model import get_now_str, get_timedelta_bystr, get_time_bystr
from lock import file_lock, file_unlock, check_lock
import matplotlib.pyplot as plt
import math
import numpy as np


# 将从txt文本中读取的字符串转变为列表
def str_to_list(line):
    temp = []
    i = 0
    j = 0
    k = 0
    length = len(line)
    while j < length:
        if (line[j] != ' ') & (k != 4) & (k != 6) & (k != 7):
            j += 1
        elif (line[j] == ' ') & (k != 4) & (k != 6) & (k != 7):
            temp.append(int(line[i:j+1]))
            j += 1
            i = j
            k += 1
        else:
            temp.append(line[i:j + 19])
            j += 20
            i = j
            k += 1
    return temp


# 将从txt文本中读取的字符串转变为列表
def str_to_list_cluster(line):
    temp1 = []
    temp2 = []
    i = 0
    j = 0
    length = len(line)
    while j < length:
        if line[j] == '|':
            temp1.append(temp2)
            temp2 = []
        if (line[i] == '[') | (line[i] == ' '):
            while 1:
                j += 1
                if (line[j] == ',') | (line[j] == ']'):
                    break
            temp2.append(int(line[i + 1:j]))
            j += 1
            i = j
        else:
            j += 1
            i += 1
    return temp1


# 更新集群资源
def update_cluster(cluster, f):
    # f = open("cluster.txt", 'w')
    for line in cluster:
        f.write(str(line) + '|')
    f.close()


pool = ["pool_1.txt", "pool_2.txt", "pool_3.txt"]
pool_lock = ["pool_1_lock.txt", "pool_2_lock.txt", "pool_3_lock.txt"]
cluster_txt = ["cluster_1.txt", "cluster_2.txt", "cluster_3.txt"]
cluster_lock = ["cluster_1_lock.txt", "cluster_2_lock.txt", "cluster_3_lock.txt"]


# 随机调度
def random_schedule():
    error = 0
    flag = [0, 0, 0]
    k = random.randint(0, 2)
    flag[k] = 1
    for i in range(3):
        """lock  pool_i.txt"""
        while check_lock(pool[i], pool_lock[i]):
            time.sleep(0.05)
        file_lock(pool[i], pool_lock[i])

        f = open(pool[i], 'r')
        if os.path.getsize(pool[i]) != 0:  # 如果不是空文件
            get_line = f.readline()  # 获取第一行
            # get_all_lines = f.readlines()  # 获取所有行
            f.close()                           # 关闭进程池文件
            """unlock pool_i.txt"""
            file_unlock(pool[i], pool_lock[i])

            temp = str_to_list(get_line)  # 字符串转列表
            """lock cluster.txt"""
            while check_lock("cluster.txt", "cluster_lock.txt"):
                time.sleep(0.05)
            file_lock("cluster.txt", "cluster_lock.txt")

            f_c = open("cluster.txt", 'r+')         # 读取集群资源
            r = f_c.readline()
            # print(r)
            # print(str_to_list_cluster(r))
            c = str_to_list_cluster(r)
            # print(c)
            while (c[k][0] < temp[2]) | (c[k][1] < temp[3]):  # 结点资源不足
                flag[k] = 1
                if (flag[0] == 1) & (flag[1] == 1) & (flag[2] == 1):
                    # print("error！ 调度失败所有结点资源均不足！")
                    error = 1
                    break
                while flag[k] == 1:
                    k = random.randint(0, 2)  # 重新选择结点但不能与之前的重复
            if error == 1:
                print("error！ 调度失败所有结点资源均不足！")
                """unlock cluster.txt"""
                file_unlock("cluster.txt", "cluster_lock.txt")
                break
            # print(get_timedelta_bystr(begin_time, get_now_str()))
            temp[6] = get_now_str()  # 修改运行时间
            temp[8] = k  # 修改部署到的结点
            """更新集群结点资源数"""
            c[k][0] -= temp[2]
            c[k][1] -= temp[3]
            # update_cluster(c, f_c)
            f_c.seek(0, 0)            # 指针指向文件起始
            f_c.truncate()            # 从指针处开始全部删除
            for line in c:
                f_c.write(str(line) + '|')
            f_c.close()
            """unlock cluster.txt"""
            file_unlock("cluster.txt", "cluster_lock.txt")
            """删除在进程池文件中的数据"""
            """lock pool_i.txt"""
            while check_lock(pool[i], pool_lock[i]):
                time.sleep(0.05)
            file_lock(pool[i], pool_lock[i])

            f_new = open(pool[i], 'r+')
            get_all_lines = f_new.readlines()
            f_new.seek(0, 0)             # 指针指向文件开始
            f_new.truncate()             # 全部删除
            for line in get_all_lines:
                if get_line == line:
                    continue
                f_new.write(line)
            f_new.close()
            """unlock pool_i.txt"""
            file_unlock(pool[i], pool_lock[i])
            """"在结点文件添加数据"""
            """lock cluster_k.txt"""
            while check_lock(cluster_txt[k], cluster_lock[k]):
                time.sleep(0.05)
            file_lock(cluster_txt[k], cluster_lock[k])

            f_w = open(cluster_txt[k], 'a')  # 打开结点文件进行添加
            for line in temp:
                f_w.write(str(line) + ' ')
            f_w.write('\n')
            f_w.close()  # 关闭集群文件
            """unlock cluster_k.txt"""
            file_unlock(cluster_txt[k], cluster_lock[k])

            print("将任务" + str(temp[0]) + "调度到结点" + str(k) + "成功！")
            break  # 退出  一次只调度一个任务
        file_unlock(pool[i], pool_lock[i])


# 贪心调度  每个结点得分是根据CPU和MEM两个得分点而来的，可能需要对CPU/MEM这个比例系数进行相关操作
def greed_schedule():
    flag = [0, 0, 0]
    rs_a = [0, 0]
    rs = []
    result = -1
    k = 0
    for i in range(3):
        """lock  pool_i.txt"""
        while check_lock(pool[i], pool_lock[i]):
            time.sleep(0.05)
        file_lock(pool[i], pool_lock[i])

        f = open(pool[i], 'r')
        if os.path.getsize(pool[i]) != 0:
            get_line = f.readline()
            f.close()                           # 关闭进程池文件
            """unlock pool_i.txt"""
            file_unlock(pool[i], pool_lock[i])

            temp = str_to_list(get_line)  # 字符串转列表
            """lock cluster.txt"""
            while check_lock("cluster.txt", "cluster_lock.txt"):
                time.sleep(0.05)
            file_lock("cluster.txt", "cluster_lock.txt")

            f_c = open("cluster.txt", 'r+')         # 读取集群资源
            r = f_c.readline()
            # print(r)
            # print(str_to_list_cluster(r))
            c = str_to_list_cluster(r)
            for j in range(3):
                if (c[j][0] < temp[2]) | (c[j][1] < temp[3]):
                    rs.append([0, 0])
                    flag[j] = 1
                else:
                    rs.append(c[j])
                    rs_a[0] += c[j][0]
                    rs_a[1] += c[j][1]
                    k += 1
            if (flag[0] == 1) & (flag[1] == 1) & (flag[2] == 1):
                print("error:调度任务"+str(temp[0])+"失败所有结点资源均不足！")
                """unlock cluster.txt"""
                file_unlock("cluster.txt", "cluster_lock.txt")
                break
            rs_a = [rs_a[0]/k, rs_a[1]/k]   # 求平均
            temp_r = [0, 0, 0]
            for k in range(3):
                if rs[k][0] > rs_a[0]:
                    temp_r[k] += pow((rs[k][0] - rs_a[0]), 2)
                else:
                    temp_r[k] -= pow((rs[k][0] - rs_a[0]), 2)
                if rs[k][1] > rs_a[1]:
                    temp_r[k] += pow((rs[k][1] - rs_a[1]), 2)
                else:
                    temp_r[k] -= pow((rs[k][1] - rs_a[1]), 2)
            print(temp_r)
            f = 0
            f_s = temp_r[0]
            for k in range(2):
                if temp_r[k+1] > f_s:
                    f_s = temp_r[k+1]
                    f = (k+1)
            temp[6] = get_now_str()
            temp[8] = f
            """更新集群结点资源数"""
            c[f][0] -= temp[2]
            c[f][1] -= temp[3]
            # update_cluster(c, f_c)
            f_c.seek(0, 0)            # 指针指向文件起始
            f_c.truncate()            # 从指针处开始全部删除
            for line in c:
                f_c.write(str(line) + '|')
            f_c.close()
            """unlock cluster.txt"""
            file_unlock("cluster.txt", "cluster_lock.txt")
            """删除在进程池文件中的数据"""
            """lock pool_i.txt"""
            while check_lock(pool[i], pool_lock[i]):
                time.sleep(0.05)
            file_lock(pool[i], pool_lock[i])

            f_new = open(pool[i], 'r+')
            get_all_lines = f_new.readlines()
            f_new.seek(0, 0)             # 指针指向文件开始
            f_new.truncate()             # 全部删除
            for line in get_all_lines:
                if get_line == line:
                    continue
                f_new.write(line)
            f_new.close()
            """unlock pool_i.txt"""
            file_unlock(pool[i], pool_lock[i])
            """"在结点文件添加数据"""
            """lock cluster_k.txt"""
            while check_lock(cluster_txt[f], cluster_lock[f]):
                time.sleep(0.05)
            file_lock(cluster_txt[f], cluster_lock[f])

            f_w = open(cluster_txt[f], 'a')  # 打开结点文件进行添加
            for line in temp:
                f_w.write(str(line) + ' ')
            f_w.write('\n')
            f_w.close()  # 关闭集群文件
            """unlock cluster_k.txt"""
            file_unlock(cluster_txt[f], cluster_lock[f])

            print("将任务" + str(temp[0]) + "调度到结点" + str(f) + "成功！")
            break  # 退出  一次只调度一个任务
        file_unlock(pool[i], pool_lock[i])


# 计算每个结点的争用率
def contention_rate(file):
    temp = []
    finish_time = []
    c_rate = 0
    f = open(file, 'r')
    if os.path.getsize(file) == 0:
        return c_rate
    else:
        lines = f.readlines()
        for line in lines:            # 格式化数据
            a = str_to_list(line)
            temp.append(a)
        now_time = get_now_str()
        for i in range(len(temp)):    # 每个进程的剩余完成时间
            b =  get_timedelta_bystr(temp[i][6], now_time)
            if b <= 0:
                finish_time.append(0)
            else:
                finish_time.append(b)
        max_time = max(finish_time)
        k = 1
        while k <= max_time:          # 计算每个时间点存在的任务数
            for i in range(len(finish_time)):
                if finish_time[i] >= k:
                    # c_rate = c_rate + 1 不考虑负载均衡
                    c_rate = c_rate + temp[i][2] + temp[i][3]  # 考虑负载均衡
            k += 1
        return c_rate


# 预测算法
def predict_schedule():
    flag = [0, 0, 0]
    c_rate = []
    for i in range(3):
        """lock  pool_i.txt"""
        while check_lock(pool[i], pool_lock[i]):
            time.sleep(0.05)
        file_lock(pool[i], pool_lock[i])

        f = open(pool[i], 'r')
        if os.path.getsize(pool[i]) != 0:
            get_line = f.readline()
            f.close()  # 关闭进程池文件
            """unlock pool_i.txt"""
            file_unlock(pool[i], pool_lock[i])

            temp = str_to_list(get_line)  # 字符串转列表
            """lock cluster.txt"""
            while check_lock("cluster.txt", "cluster_lock.txt"):
                time.sleep(0.05)
            file_lock("cluster.txt", "cluster_lock.txt")

            f_c = open("cluster.txt", 'r+')  # 读取集群资源
            r = f_c.readline()
            # print(r)
            # print(str_to_list_cluster(r))
            c = str_to_list_cluster(r)
            for j in range(3):
                if (c[j][0] < temp[2]) | (c[j][1] < temp[3]):
                    c_rate.append(0x3f3f3f)  # 争用率设为无穷大
                    flag[j] = 1
                else:
                    """lock cluster_j.txt"""
                    while check_lock(cluster_txt[j], cluster_lock[j]):
                        time.sleep(0.05)
                    file_lock(cluster_txt[j], cluster_lock[j])

                    # file = open(cluster_txt[j], 'r')
                    file = cluster_txt[j]
                    a = contention_rate(file)
                    c_rate.append(a)
                    """unlock cluster_j.txt"""
                    file_unlock(cluster_txt[j], cluster_lock[j])
            if (flag[0] == 1) & (flag[1] == 1) & (flag[2] == 1):
                print("error:调度任务" + str(temp[0]) + "失败所有结点资源均不足！")
                """unlock cluster.txt"""
                file_unlock("cluster.txt", "cluster_lock.txt")
                break
            k = c_rate.index(min(c_rate))  # 获取最小争用率的结点

            temp[6] = get_now_str()  # 修改运行时间
            temp[8] = k  # 修改部署到的结点
            """更新集群结点资源数"""
            c[k][0] -= temp[2]
            c[k][1] -= temp[3]
            # update_cluster(c, f_c)
            f_c.seek(0, 0)  # 指针指向文件起始
            f_c.truncate()  # 从指针处开始全部删除
            for line in c:
                f_c.write(str(line) + '|')
            f_c.close()
            """unlock cluster.txt"""
            file_unlock("cluster.txt", "cluster_lock.txt")
            """删除在进程池文件中的数据"""
            """lock pool_i.txt"""
            while check_lock(pool[i], pool_lock[i]):
                time.sleep(0.05)
            file_lock(pool[i], pool_lock[i])

            f_new = open(pool[i], 'r+')
            get_all_lines = f_new.readlines()
            f_new.seek(0, 0)  # 指针指向文件开始
            f_new.truncate()  # 全部删除
            for line in get_all_lines:
                if get_line == line:
                    continue
                f_new.write(line)
            f_new.close()
            """unlock pool_i.txt"""
            file_unlock(pool[i], pool_lock[i])
            """"在结点文件添加数据"""
            """lock cluster_k.txt"""
            while check_lock(cluster_txt[k], cluster_lock[k]):
                time.sleep(0.05)
            file_lock(cluster_txt[k], cluster_lock[k])

            f_w = open(cluster_txt[k], 'a')  # 打开结点文件进行添加
            for line in temp:
                f_w.write(str(line) + ' ')
            f_w.write('\n')
            f_w.close()  # 关闭集群文件
            """unlock cluster_k.txt"""
            file_unlock(cluster_txt[k], cluster_lock[k])

            print("将任务" + str(temp[0]) + "调度到结点" + str(k) + "成功！")
            break  # 退出  一次只调度一个任务
        file_unlock(pool[i], pool_lock[i])


class ACO(object):
    def __init__(self, tasks, cluster, ants_num=10, times=100):
        self.CPU_MAX = 100
        self.MEM_MAX = 100
        self.tasks = tasks
        self.cluster = cluster
        self.tasks_num = len(tasks)  # 任务数量
        self.cluster_num = 3  # 集群节点数量
        self.ants_num = ants_num  # 蚂蚁数量
        self.times = times  # 迭代次数
        # 信息素（用于每次迭代） 初始化用剩余资源量表示
        self.pheromone = [cluster[0][0] / self.CPU_MAX + cluster[0][1] / self.MEM_MAX,
                          cluster[0][0] / self.CPU_MAX + cluster[0][1] / self.MEM_MAX,
                          cluster[0][0] / self.CPU_MAX + cluster[0][1] / self.MEM_MAX]
        # 食物素（用于为每个任务选择节点）用剩余资源量表示
        self.food = None
        # [[cluster[0][0], cluster[0][1]],[cluster[0][0], cluster[0][1]],[cluster[0][0], cluster[0][1]]]
        self.hf_i_j = None  # 蚂蚁为任务i选择节点j的启发因子(剩余资源量+均衡度）
        self.ihj = 2  # 信息启发因子
        self.ehj = 4  # 期望启发因子
        self.pe = 0.3  # 信息素挥发因子
        self.best_schedule = None  # 最优调度
        self.part_best_schedule = None
        self.best_fitness = 0

    # p是为任务i选择节点j的概率列表。 例如：[0.2, 0.3, 0.5] 采用轮盘赌的策略进行选择
    def select_i_j(self, p):
        x = random.uniform(0, 1)
        if x < p[0]:
            return 0
        elif x - p[0] < p[1]:
            return 1
        else:
            return 2

    # 概率计算  flag用于说明那些节点不能选 例如：flag = [1,1,0]三号节点资源不足不能选
    def calculate_p(self, flag):
        p = []
        temp = []  # 计算中间值Π^α*μ^θ
        temp_sum = 0
        for i in range(self.cluster_num):
            if flag == 0:
                temp.append(0)
            else:
                c = self.food[i][0] / self.CPU_MAX
                m = self.food[i][1] / self.MEM_MAX
                # self.hf_i_j = (c + m) / 2 + (1 - abs(c - m))
                self.hf_i_j = (c + m) + (1 - abs(c - m))
                temp.append((pow(self.pheromone[i], self.ihj)) * pow(self.hf_i_j, self.ehj))
        for k in range(self.cluster_num):
            temp_sum += temp[k]
        for j in range(self.cluster_num):
            if flag[j] == 0:
                p.append(0)
            else:
                p.append(temp[j] / temp_sum)
        return p

    # 生成解向量  """未考虑资源不足情况"""
    def solution_vector(self):
        # 初始化食物素
        self.food = [[self.cluster[0][0], self.cluster[0][1]],
                     [self.cluster[1][0], self.cluster[1][1]],
                     [self.cluster[2][0], self.cluster[2][1]]]
        flag = [0, 0, 0]
        solution = [-1 for _ in range(self.tasks_num)]  # 初始化解向量
        for i in range(self.tasks_num):
            for j in range(self.cluster_num):
                if (self.tasks[i][2] < self.food[j][0]) | (self.tasks[i][3] < self.food[j][1]):
                    flag[j] = 1
            if flag == [0, 0, 0]:
                break
            p = self.calculate_p(flag)  # 计算概率
            point = self.select_i_j(p)  # 选择节点
            solution[i] = point
            # 更新食物素
            self.food[point][0] -= self.tasks[i][2]
            self.food[point][1] -= self.tasks[i][3]
        return solution

    # 评估解向量   根据异构资源间的均衡和异构资源内的均衡
    def evaluate_solution(self) -> float:
        cpu_util = []
        mem_util = []
        for i in range(self.cluster_num):
            cpu_util.append(self.food[i][0])
            mem_util.append(self.food[i][1])
        return np.std(cpu_util, ddof=1) + np.std(mem_util, ddof=1)  \
               + np.std(self.food[0], ddof=1)/3 + np.std(self.food[1], ddof=1)/3 + np.std(self.food[2], ddof=1)/3

    # 适应度 目标函数
    def fitness(self):
        return 1 / self.evaluate_solution()

    # 信息素更新
    def update_pheromone(self, v, flag):
        add_pheromone = [0, 0, 0]
        for i in range(self.tasks_num):
            for j in range(self.cluster_num):
                if j == v[i]:
                    add_pheromone[j] += (self.tasks[i][2]/self.CPU_MAX + self.tasks[i][3]/self.MEM_MAX)/2

        if flag == 0:
            for k in range(self.cluster_num):
                self.pheromone[k] = (1-self.pe)*self.pheromone[k] + 0.2*add_pheromone[k]
        else:
            for k in range(self.cluster_num):
                self.pheromone[k] = (1-self.pe)*self.pheromone[k] + 0.35*add_pheromone[k]

    def aco_schedule(self):
        results = [0 for _ in range(self.times)]
        for i in range(self.times):
            part_best_fitness = 0
            for ant in range(self.ants_num):
                a = self.solution_vector()
                fitness = self.fitness()
                if fitness > part_best_fitness:
                    self.part_best_schedule = a
                    part_best_fitness = fitness
            # print(self.part_best_schedule, "+", part_best_fitness)
            if self.best_fitness > part_best_fitness:
                self.update_pheromone(self.part_best_schedule, 0)
            else:
                self.best_fitness = part_best_fitness
                self.best_schedule = self.part_best_schedule
                self.update_pheromone(self.part_best_schedule, 1)  # 如果更新了全局最优解那么留下的信息素更多
            results[i] = part_best_fitness
        return results


def aco_schedule():
    """pool_1 = []
    pool_2 = []
    pool_3 = []
    pool_all = [pool_1, pool_2, pool_3]"""
    tasks = []
    for i in range(3):
        """lock pool_i.txt"""
        while check_lock(pool[i], pool_lock[i]):
            time.sleep(0.05)
        file_lock(pool[i], pool_lock[i])
        f = open(pool[i], 'r')
        if os.path.getsize(pool[i]) != 0:
            get_lines = f.readlines()
            for j in get_lines:
                temp = str_to_list(j)
                tasks.append(temp)
            f.close()
            """unlock pool_i.txt"""
            file_unlock(pool[i], pool_lock[i])
        """unlock pool_i.txt"""
        file_unlock(pool[i], pool_lock[i])
    # print(tasks)
    if tasks:
        """lock cluster.txt"""
        while check_lock("cluster_txt", "cluster_lock.txt"):
            time.sleep(0.05)
        file_lock("cluster.txt", "cluster_lock.txt")
        f_c = open("cluster.txt", 'r+')

        r = f_c.readline()
        c = str_to_list_cluster(r)
        ac = ACO(tasks, c)
        res = ac.aco_schedule()
        """更新集群节点资源"""
        t = get_now_str()
        schedule_task = []
        # print(ac.best_schedule)
        pool_1 = []
        pool_2 = []
        pool_3 = []
        pool_all = [pool_1, pool_2, pool_3]
        for k in range(len(ac.best_schedule)):
            point = ac.best_schedule[k]
            if point != -1:           # 调度成功的任务
                c[point][0] -= tasks[k][2]
                c[point][1] -= tasks[k][3]
                #a = tasks[k]
                pool_all[tasks[k][1]-1].append(tasks[k])
                # print(pool_all[point])
                # print(tasks[k])
                tasks[k][8] = point
                tasks[k][6] = t
                print("任务 ", tasks[k][0], "调度到节点 ", point)
                schedule_task.append(tasks[k])
        # print(pool_all)
        f_c.seek(0, 0)
        f_c.truncate()
        for line in c:
            f_c.write(str(line) + '|')
        f_c.close()
        "unlock cluster.txt"
        file_unlock("cluster.txt", "cluster_lock.txt")
        """删除在进程池文件中的数据"""
        for i in range(3):
            if pool_all[i]:
                for t in range(len(pool_all[i])):
                    """lock pool_i.txt"""
                    while check_lock(pool[i], pool_lock[i]):
                        time.sleep(0.05)
                    file_lock(pool[i], pool_lock[i])

                    f_i = open(pool[i], 'r+')
                    get_all_lines = f_i.readlines()
                    f_i.seek(0, 0)
                    f_i.truncate()
                    for line in get_all_lines:
                        line_r = str_to_list(line)
                        if pool_all[i][t][0] == line_r[0]:
                            continue
                        f_i.write(line)
                    f_i.close()
                    """unlock pool_i.txt"""
                    file_unlock(pool[i], pool_lock[i])
        """添加到集群节点"""
        c_1 = []
        c_2 = []
        c_3 = []
        c_all = [c_1, c_2, c_3]
        for line in schedule_task:
            if line[8] == 0:
                c_1.append(line)

            elif line[8] == 1:
                c_2.append(line)
            elif line[8] == 2:
                c_3.append(line)
        for i in range(3):
            if c_all[i]:
                """lock cluster_i.txt"""
                while check_lock(cluster_txt[i], cluster_lock[i]):
                    time.sleep(0.05)
                file_lock(cluster_txt[i], cluster_lock[i])

                f_c_i = open(cluster_txt[i], 'a')
                for line_1 in c_all[i]:
                    for line_2 in line_1:
                        f_c_i.write(str(line_2) + ' ')
                    f_c_i.write('\n')
                f_c_i.close()
                """unlock cluster_i.txt"""
                file_unlock(cluster_txt[i], cluster_lock[i])


def main():
    while 1:
        time.sleep(3)
        # random_schedule()
        # greed_schedule()
        # predict_schedule()
        aco_schedule()
        # print("1111")


if __name__ == '__main__':
    main()
