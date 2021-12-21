import matplotlib.pyplot as plt

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

# f = open("CPU_MEM_use_random.txt", 'r')
# f = open("CPU_MEM_use_greed.txt", 'r')
# f = open("CPU_MEM_use_predict.txt", 'r')
f =open("CPU_MEM_use_aco.txt", 'r')
lines = f.readlines()
times = len(lines)
result_cpu_1 = []
result_mem_1 = []
result_cpu_2 = []
result_mem_2 = []
result_cpu_3 = []
result_mem_3 = []
for line in lines:
    temp = str_to_list_cluster(line)
    result_cpu_1.append(temp[0][0])
    result_mem_1.append(temp[0][1])
    result_cpu_2.append(temp[1][0])
    result_mem_2.append(temp[1][1])
    result_cpu_3.append(temp[2][0])
    result_mem_3.append(temp[2][1])

plt.subplot(212)
plt.plot(range(times), result_cpu_1, label = '节点1')
plt.plot(range(times), result_cpu_2, linestyle = '--', label = '节点2')
plt.plot(range(times), result_cpu_3, linestyle = '-.', label = '节点3')
plt.xlabel("时间")
plt.ylabel("CPU利用率%")
plt.rcParams['font.sans-serif'] = ['KaiTi']


plt.subplot(211)
plt.plot(range(times), result_mem_1, label = '节点1')
plt.plot(range(times), result_mem_2, linestyle = '--', label = '节点2')
plt.plot(range(times), result_mem_3, linestyle = '-.', label = '节点3')

plt.xlabel("时间")
plt.ylabel("MEM利用率%")
plt.rcParams['font.sans-serif'] = ['KaiTi']
# plt.title("随机算法CPU/MEM利用率")
# plt.title("贪心算法CPU/MEM利用率")
# plt.title("预测算法CPU/MEM利用率")
plt.title("蚁群算法CPU/MEM利用率")
plt.legend()
plt.show()