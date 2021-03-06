**python** **模拟多集群调度的任务调度器**

###### 2021/12/3 进展

基本框架框架已搭建完全（初始化、任务创建、任务调度（from进程池to集群结点）、完成队列（资源释放）、监控单元）

基于文件实现的文件锁（windows无fcntl等库）

待做：

1. 集群资源动态可视化未做，评估调度优劣的模块未做（CPU利用率，MEM利用率，平均周转时间...）

2. 只实现了简单的随机调度，未来将实现基于启发式算法的调度

###### 2021/12/5 进展

新增了贪心调度和预测调度，大致写了下评测模块

###### 2021/12/13 进展

添加了启发式算法（蚁群算法）
具体细节见ACO类

###### 2021/12/21 进展

修改了几个算法的bug，简单做了下在资源充足和资源不充足情况下各类算法性能的展示

资源充足情况下：
![image](https://user-images.githubusercontent.com/60082323/146951973-6cdce9bb-3c42-4292-8fed-349c578069db.png)
![image](https://user-images.githubusercontent.com/60082323/146952051-c2949642-9096-4a81-93db-5af990d5336d.png)
![image](https://user-images.githubusercontent.com/60082323/146952081-7d9268b7-7b72-4dc9-bdfc-062d0399a4a1.png)
![image](https://user-images.githubusercontent.com/60082323/146952096-cbe1d339-55ff-4e9e-8a73-d8a62ac069cc.png)
通过方差计算各类算法的资源均衡度

随机算法：CPU：4.9；MEM：5.7

贪心算法：CPU：2.7；MEM：2.3

预测算法：CPU: 2.5; MEM: 2.5

蚁群算法：CPU: 2.0；MEM：1.9

资源不充足情况下通过平均周转时间和吞吐量评估各类算法：

随机算法：31.7		      75/min

贪心算法：33.8			      71/min

改进的贪心算法：31.2		      73/min

预测算法：32.8			       72/min

蚁群算法：29.7			       81/min
