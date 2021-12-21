# 初始化锁文件
def ini_locks(lock_name):
    f = open(lock_name, 'w')
    f.write('0')
    f.close()


# 更新集群资源
def update_cluster(cluster):
    f = open("cluster.txt", 'w')
    for line in cluster:
        f.write(str(line) + '|')
    f.close()


def ini_file(file):
    f = open(file, 'w')
    f.seek(0, 0)
    f.truncate()

def main():
    cluster_1 = [100, 100]
    cluster_2 = [100, 100]
    cluster_3 = [100, 100]
    cluster = [cluster_1, cluster_2, cluster_3]
    pool = ["pool_1.txt", "pool_2.txt", "pool_3.txt"]
    cluster_txt = ["cluster_1.txt", "cluster_2.txt", "cluster_3.txt"]
    pool_lock = ["pool_1_lock.txt", "pool_2_lock.txt", "pool_3_lock.txt"]
    cluster_lock = ["cluster_1_lock.txt", "cluster_2_lock.txt", "cluster_3_lock.txt"]
    """初始化进程池锁"""
    for i in range(len(pool_lock)):
        ini_locks(pool_lock[i])
    """初始化集群结点锁"""
    for j in range(len(cluster_lock)):
        ini_locks(cluster_lock[j])
    """初始化集群监控资源锁"""
    ini_locks("cluster_lock.txt")
    """初始化集群资源"""
    update_cluster(cluster)
    """初始化进程池、节点文件"""
    for k in range(3):
        ini_file(pool[k])
        ini_file(cluster_txt[k])



if __name__ == '__main__':
    main()
