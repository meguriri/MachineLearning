import zerorpc
import pandas as pd
import argparse
import random

def createSampleDataset(filename,batchSize):
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
    random_numbers = random.sample(range(0, len(labelType)), 5)
    dataset = pd.read_csv(filename, header=None, sep=', ',engine='python')
    dataset = dataset[~dataset.isin(['?']).any(axis=1)]
    dataset = dataset.sample(n=batchSize)
    dataset = dataset.values.tolist()
    sampleDataset = [[row[i] for i in random_numbers] for row in dataset]
    for i in range(len(sampleDataset)):
        sampleDataset[i].append(dataset[i][-1])
    sampleLabels = []
    sampleLabelType = []
    for i in random_numbers:
        sampleLabels.append(labels[i])
        sampleLabelType.append(labelType[i])
    return sampleDataset, sampleLabels, sampleLabelType

def getAnswer(testList):
    testDataset = pd.read_csv('./adult/adult.test', header=None, sep=', ',engine='python')
    testDataset = testDataset[~testDataset.isin(['?']).any(axis=1)]
    testDataset = testDataset.values.tolist()
    correct = 0
    error = 0
    for i in range(len(testDataset)):
        c1 = 0
        c2 = 0
        for j in range(len(testList)):
            if testList[j][i] == '<=50K.':
                c1 += 1
            else:
                c2 += 1
        answer = '<=50K.' if c1 > c2 else '>50K.'
        if answer == testDataset[i][-1]:
            correct += 1
        else:
            error += 1
    print('Correct: {},Error: {},Accuracy: {}'.format(correct, error, correct / len(testDataset)))

class MyRPCServer:
    testList = []
    def __init__(self,filePath,clientNum, batchSize):
        self.filePath = filePath
        self.clientNum = clientNum
        self.batchSize = batchSize

    def getDataSet(self):
        dataset, labels, labelType = createSampleDataset(self.filePath,self.batchSize)
        return dataset, labels, labelType

    def commitTest(self, test):
        self.testList.append(test)
        # print('get test', test)
        if len(self.testList) == self.clientNum:
            print('all test is ok')
            getAnswer(self.testList)
            # raise SystemExit  # 或者其他方法关闭服务器

if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()
    # 添加命令行参数
    parser.add_argument('-d','--dataset', type=str, help='dataset filepath')
    parser.add_argument('-n','--num', type=int, help='Age of the user', required=False,default=10)
    parser.add_argument('-b','--batch', type=int, help='batch size',required=False,default=5000)
    # 解析命令行参数
    args = parser.parse_args()

    # 创建RPC服务器
    server = zerorpc.Server(MyRPCServer(args.dataset,args.num,args.batch))
    server.bind("tcp://0.0.0.0:4242")
    # 启动服务器
    server.run()

