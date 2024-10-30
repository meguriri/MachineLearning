import zerorpc
import pandas as pd
import tree as t 

# 创建RPC客户端
client = zerorpc.Client()
client.connect("tcp://0.0.0.0:4242")  # 连接到服务器地址

# 调用远程函数
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
sampleDataset, sampleLabels, sampleLabelType = client.getDataSet()
nowLabels = sampleLabels[:]
nowLabelType = sampleLabelType[:]
tree = t.train(sampleDataset, nowLabels, nowLabelType)
print('train ok')
testList = t.newTest(tree, './adult/adult.test', labels, labelType)
client.commitTest(testList)
