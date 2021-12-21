import time
import numpy as np
from lock import file_lock, file_unlock, check_lock
from time_model import get_timedelta_bystr, get_time_bystr


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
            temp.append(int(line[i:j + 1]))
            j += 1
            i = j
            k += 1
        else:
            temp.append(line[i:j + 19])
            j += 20
            i = j
            k += 1
    return temp


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


# 求均衡  集群整体目前使用的是方差  可以改  结点异构资源间的均衡1-abs（CPU-MEM）
def balance(c_1, c_2, c_3):
    """集群整体的各部分资源均衡， 越接近0越好"""
    t = [[c_1[0], c_2[0], c_3[0]], [c_1[1], c_2[1], c_3[1]]]
    var = [np.var(t[0]), np.var(t[1])]
    """结点资源的异构资源均衡水平， 越接近1越好"""
    c_x_b = [1 - abs(c_1[0] - c_1[1]), 1 - abs(c_2[0] - c_2[1]), 1 - abs(c_3[0] - c_3[1])]
    b = var + c_x_b
    return b


# CPU/MEM使用率 & 资源均衡 [[], [], [], []]前三个是结点的使用率，第四个是均衡
def usage_rate():
    ini = [[20, 20], [20, 20], [20, 20]]
    while check_lock("cluster.txt", "cluster_lock.txt"):
        time.sleep(0.05)
    file_lock("cluster.txt", "cluster_lock.txt")
    f = open("cluster.txt", 'r')
    line = f.readline()
    file_unlock("cluster.txt", "cluster_lock.txt")
    data = str_to_list_cluster(line)
    c_1_rate = [(ini[0][0] - data[0][0]) / ini[0][0], (ini[0][1] - data[0][1])/ini[0][1]]
    c_2_rate = [(ini[1][0] - data[1][0]) / ini[1][0], (ini[1][1] - data[1][1])/ini[1][1]]
    c_3_rate = [(ini[2][0] - data[2][0]) / ini[2][0], (ini[2][1] - data[2][1])/ini[2][1]]
    c_balance = balance(c_1_rate, c_2_rate, c_3_rate)
    result = [c_1_rate, c_2_rate, c_3_rate, c_balance]
    return result


# 平均周转时间
def ATT():
    f = open("finish.txt", 'r')
    lines = f.readlines()
    k = 0
    sum = 0
    for line in lines:
        a = str_to_list(line)
        time1 = a[4]  # 创建时间
        time2 = a[7]  # 完成时间
        tt = get_timedelta_bystr(time1, time2)
        sum += tt
        k += 1
    return sum/k


def a():
    bla_1 = 0
    bla_2 = 0
    # f = open("CPU_MEM_use_random.txt", 'r')
    f = open("CPU_MEM_use_greed.txt", 'r')
    # f = open("CPU_MEM_use_predict.txt", 'r')
    # f = open("CPU_MEM_use_aco.txt", 'r')
    lines = f.readlines()
    len_1 = len(lines)
    for line in lines:
        c = str_to_list_cluster(line)
        cpu = [c[0][0], c[1][0], c[2][0]]
        mem = [c[0][1], c[1][1], c[2][1]]
        bla_1 += np.std(cpu, ddof=1)
        bla_2 += np.std(mem, ddof=1)
    print(bla_1/len_1)
    print(bla_2/len_1)


def b():
    bla_1 = 0
    bla_2 = 0
    # f = open("CPU_MEM_use_random.txt", 'r')
    # f = open("CPU_MEM_use_greed.txt", 'r')
    # f = open("CPU_MEM_use_predict.txt", 'r')
    f = open("CPU_MEM_use_aco.txt", 'r')
    lines = f.readlines()
    len_1 = len(lines)
    for line in lines:
        c = str_to_list_cluster(line)
        cpu = [100 - c[0][0], 100 - c[1][0], 100 - c[2][0]]
        mem = [100 - c[0][1], 100 - c[1][1], 100 - c[2][1]]
        # bla_1 += np.std(cpu, ddof=1)
        # bla_2 += np.std(mem, ddof=1)
        bla_1 += (cpu[0]+cpu[1]+cpu[2])/3
        bla_2 += (mem[0]+mem[1]+mem[2])/3
    print(bla_1/len_1)
    print(bla_2/len_1)
def main():
    att = ATT()
    c_r = usage_rate()
    print(att)
    # print(c_r)


if __name__ == '__main__':
    # while 1:
        # time.sleep(1)
    # main()
    # a()
    b()
