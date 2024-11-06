'''
    client.py
    RPC客户端，负责执行决策树模型训练任务，并将训练好的决策树发送给主节点（服务端）
'''
import zerorpc
import pandas as pd
import tree as t 


class Worker:
    # 构造函数
    def __init__(self,server_address="tcp://0.0.0.0:4242"):
        self.client = zerorpc.Client()
        self.client.connect(server_address)

    # 训练模型的方法
    def train_model(self,sampleDataset,sampleLabels,sampleLabelType):
        # 获取标签和特征类型
        nowLabels = sampleLabels[:]
        nowLabelType = sampleLabelType[:]
        # 调用tree包的train方法，训练决策树
        tree = t.train(sampleDataset, nowLabels, nowLabelType)
        return tree
    
    # 客户端启动方法
    def run(self):
        i = 1
        # 循环向服务端发起请求，不断获取训练任务，直到服务端全部任务都完成
        while True:
            print('start ',i)
            # 调用getDataSet()方法获取训练数据集
            sampleDataset, sampleLabels, sampleLabelType = self.client.getDataSet()
            # 如果为None，则表示没有任务了，直接结束
            if sampleDataset is None:
                break
            print('get dataset ok')
            # 训练决策树模型
            tree = self.train_model(sampleDataset,sampleLabels,sampleLabelType)
            print('train ok')
            # 调用CommitTree()方法将决策树模型发送给服务端
            self.client.commitTree(tree)
            print('commit tree ok')
            # 清除临时变量缓存
            del(tree)
            del(sampleDataset)
            i+=1

if __name__ == "__main__":
    worker = Worker()
    worker.run()
