import os.path
from time_model import get_now_str, get_time_bystr, get_timedelta_bystr, get_time_finish
import time
from lock import file_lock, file_unlock, check_lock


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


def process_finish(now_time, cluster_x, cluster_x_lock):
    finish = []
    delete = []
    flag = 0  # 用于判断是否需要归还资源
    """lock cluster_x.txt"""
    while check_lock(cluster_x, cluster_x_lock):
        time.sleep(0.05)
    file_lock(cluster_x, cluster_x_lock)

    f = open(cluster_x, 'r+')
    if os.path.getsize(cluster_x) != 0:   # 不是空文件
        lines = f.readlines()
        print(lines)
        f.close()
        """unlock cluster_x.txt"""
        file_unlock(cluster_x, cluster_x_lock)
        for line in lines:
            k = line
            print(k)
            temp = str_to_list(line)
            print(temp)
            a = temp[6]
            print(a)
            b = temp[5]
            if get_timedelta_bystr(a, now_time) >= b:
                # finish_time = get_time_finish(a, b)
                finish_time = now_time
                temp[7] = finish_time
                finish.append(temp)
                delete.append(k)
        print(finish)
        """将完成的任务从结点中删除"""
        for i in delete:
            """lock cluster_x.txt"""
            while check_lock(cluster_x, cluster_x_lock):
                time.sleep(0.05)
            file_lock(cluster_x, cluster_x_lock)

            f_w2 = open(cluster_x, 'r+')
            lines_r = f_w2.readlines()
            f_w2.seek(0, 0)
            f_w2.truncate()
            for j in lines_r:
                if i == j:
                    flag += 1
                    continue
                f_w2.write(j)
            f_w2.close()
            """unlock cluster_x.txt"""
            file_unlock(cluster_x, cluster_x_lock)
        """将完成的任务添加到完成队列"""
        f_w1 = open("finish.txt", 'a')
        for i in finish:
            for j in i:
                f_w1.write(str(j) + ' ')
            f_w1.write('\n')
        f_w1.close()
        """归还资源"""
        if flag != 0:
            """统计资源"""
            cpu = [0, 0, 0]
            mem = [0, 0, 0]
            for i in finish:
                if i[8] == 0:
                    cpu[0] += i[2]
                    mem[0] += i[3]
                elif i[8] == 1:
                    cpu[1] += i[2]
                    mem[1] += i[3]
                elif i[8] == 2:
                    cpu[2] += i[2]
                    mem[2] += i[3]
            print(cpu)
            print(mem)
            """归还资源"""
            """lock cluster.txt"""
            while check_lock("cluster.txt", "cluster_lock.txt"):
                time.sleep(0.05)
            file_lock("cluster.txt", "cluster_lock.txt")

            f_r_w = open("cluster.txt", 'r+')
            line = f_r_w.readline()
            # f_r.close()
            list_line = str_to_list_cluster(line)
            print(list_line)
            for k in range(3):
                list_line[k][0] += cpu[k]
                list_line[k][1] += mem[k]
            # f_w3 = open("cluster.txt", 'w')
            f_r_w.seek(0,0)
            f_r_w.truncate()
            for line in list_line:
                f_r_w.write(str(line) + '|')
            f_r_w.close()
            """unlock cluster.txt"""
            file_unlock("cluster.txt", "cluster_lock.txt")
    f.close()
    """unlock cluster_x.txt"""
    file_unlock(cluster_x, cluster_x_lock)

def main():
    while 1:
        time.sleep(1)
        now_time = get_now_str()
        process_finish(now_time=now_time, cluster_x="cluster_1.txt", cluster_x_lock="cluster_1_lock.txt")
        process_finish(now_time=now_time, cluster_x="cluster_2.txt", cluster_x_lock="cluster_2_lock.txt")
        process_finish(now_time=now_time, cluster_x="cluster_3.txt", cluster_x_lock="cluster_3_lock.txt")


if __name__ == '__main__':
    main()
