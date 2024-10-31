import zerorpc
import pandas as pd
import tree as t 

labels = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
              'marital-status', 'occupation',
              'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week',
              'native-country']
labelType = ['continuous', 'uncontinuous', 'continuous',
                 'uncontinuous',
                 'continuous', 'uncontinuous',
                 'uncontinuous', 'uncontinuous', 'uncontinuous',
                 'uncontinuous', 'continuous', 'continuous',
                 'continuous', 'uncontinuous']

class Worker:
    def __init__(self,server_address="tcp://0.0.0.0:4242"):
        self.client = zerorpc.Client()
        self.client.connect(server_address)
    def train_model(self,sampleDataset,sampleLabels,sampleLabelType):
        nowLabels = sampleLabels[:]
        nowLabelType = sampleLabelType[:]
        tree = t.train(sampleDataset, nowLabels, nowLabelType)
        return tree
    
    def run(self):
        i = 1
        while True:
            print('start ',i)
            sampleDataset, sampleLabels, sampleLabelType = self.client.getDataSet()
            if sampleDataset is None:
                break
            print('get dataset ok')
            tree = self.train_model(sampleDataset,sampleLabels,sampleLabelType)
            print('train ok')
            testList = t.newTest(tree, './adult/adult.test', labels, labelType)
            self.client.commitTest(testList)
            print('commit test ok')
            del(tree)
            del(sampleDataset)
            del(testList)
            i+=1
# 创建RPC客户端
# client = zerorpc.Client()
# client.connect("tcp://192.168.235.205:4242")  # 连接到服务器地址

# 调用远程函数

# sampleDataset, sampleLabels, sampleLabelType = client.getDataSet()
# nowLabels = sampleLabels[:]
# nowLabelType = sampleLabelType[:]
# tree = t.train(sampleDataset, nowLabels, nowLabelType)
# print('train ok')
# testList = t.newTest(tree, './adult/adult.test', labels, labelType)
# client.commitTest(testList)
if __name__ == "__main__":
    worker = Worker()
    worker.run()
