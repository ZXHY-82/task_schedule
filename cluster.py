import random
import time
import os
from time_model import get_now_str, get_timedelta_bystr, get_time_bystr
from lock import file_lock, file_unlock, check_lock
# from process_pool import begin_time


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

"""
cluster_1 = [20, 20]
cluster_2 = [20, 20]
cluster_3 = [20, 20]
cluster = [cluster_1, cluster_2, cluster_3]
# 初始化集群资源
update_cluster(cluster)
"""
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

def main():
    while 1:
        time.sleep(1)
        random_schedule()


if __name__ == '__main__':
    main()
