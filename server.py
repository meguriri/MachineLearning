'''
    server.py
    RPC服务端，负责向训练端发送训练数据集和参数，并接受训练端训练好的决策树模型
'''
import zerorpc
import argparse
import threading
from tree import forestTest,storeTree,createSampleDataset

class Manager:
    # 构造函数，传入训练集位置，训练端节点数，和训练数据大小
    def __init__(self,filePath,clientNum,batchSize):
        self.ok = 0
        self.filePath = filePath
        self.clientNum = clientNum
        self.lock = threading.Lock()
        self.batchSize = batchSize
        self.forest = []

    # 获取数据集和参数的RPC方法
    def getDataSet(self):
        with self.lock:
            # 当训练任务全部完成后返回None
            if self.ok >= self.clientNum:
                return None,None,None
            # 调用tree包的createSampleDataset方法生成数据集
            dataset, labels, labelType = createSampleDataset(self.filePath,self.batchSize)
            return dataset, labels, labelType

    # 接受训练端决策树模型的RPC方法
    def commitTree(self, tree):
        with self.lock:
            # 将决策树添加到森林中
            self.forest.append(tree)
            # 将决策树保存在本地
            storeTree(tree,fileName="./forest/tree_"+str(self.ok)+'.txt')
            print('now ok:',self.ok)
            # 增加一个完成的任务
            self.ok+=1
            # 当训练任务全部完成后返回None
            if  self.ok > self.clientNum:
                return None
            # 当训练全部完成后执行随机森林的测试
            if self.ok == self.clientNum:
                print('all tree is ok')
                forestTest(self.forest)

    # 服务端结束的方法
    def stop(self):    
        self.server.close()
        print('server is close')

    # 服务端启动的方法
    def run(self):
        self.server = zerorpc.Server(self)
        self.server.bind("tcp://0.0.0.0:4242")
        print('server is start,wait connect...',self.clientNum)
        self.server.run()

if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()
    # 添加命令行参数
    parser.add_argument('-d','--dataset', type=str, help='dataset filepath')
    parser.add_argument('-n','--num', type=int, help='Age of the user', required=False,default=10)
    parser.add_argument('-b','--batch', type=int, help='batch size',required=False,default=5000)
    # 解析命令行参数
    args = parser.parse_args()

    # 启动服务端
    manager = Manager(args.dataset,args.num,args.batch)
    manager.run()


