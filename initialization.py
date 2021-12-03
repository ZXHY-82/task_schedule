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


def main():
    cluster_1 = [20, 20]
    cluster_2 = [20, 20]
    cluster_3 = [20, 20]
    cluster = [cluster_1, cluster_2, cluster_3]
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


if __name__ == '__main__':
    main()
