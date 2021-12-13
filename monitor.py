import time
from time_model import get_now_str
from lock import file_lock, file_unlock, check_lock


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


while 1:
    time.sleep(1)
    while check_lock("cluster.txt", "cluster_lock.txt"):
        time.sleep(0.05)
    file_lock("cluster.txt", "cluster_lock.txt")

    f = open("cluster.txt", "r+")
    line = f.readline()
    temp = str_to_list_cluster(line)
    t = get_now_str()
    print("当前时间 " + t + " 集群资源如下：" + "结点0剩余资源[CPU:" + str(temp[0][0]) + " MEM:" + str(temp[0][1]) + \
          "] 结点1剩余资源[CPU:" + str(temp[1][0]) + " MEM:" + str(temp[1][1]) + \
          "] 结点2剩余资源[CPU:" + str(temp[2][0]) + " MEM:" + str(temp[2][1]) + "]")
    f.close()
    file_unlock("cluster.txt", "cluster_lock.txt")
