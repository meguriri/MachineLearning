import zerorpc
import pandas as pd
import argparse
import random
import threading
from tree import labels,labelType,forestTest
import tree as t



def createSampleDataset(filename,batchSize):
    random_numbers = random.sample(range(0, len(labelType)), 4)
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

class Manager:
    def __init__(self,filePath,clientNum,batchSize):
        self.testList = []
        self.ok = 0
        self.filePath = filePath
        self.clientNum = clientNum
        self.lock = threading.Lock()
        self.batchSize = batchSize
        # self.dataLoaded = False
        # self.loadAndSplitData(self,filePath)

    def getDataSet(self):
        # with self.lock:
            if self.ok == self.clientNum:
                return None,None,None
            dataset, labels, labelType = createSampleDataset(self.filePath,self.batchSize)
            return dataset, labels, labelType

    def commitTest(self, test):
        # with self.lock:
            self.ok+=1
            self.testList.append(test)
            print('now ok:',self.ok)
            # print('get test', test)
            if self.ok == self.clientNum:
                print('all test is ok')
                getAnswer(self.testList)
                # self.stop()

    def stop(self):    
        self.server.close()
        print('server is close')

    def run(self):
        self.server = zerorpc.Server(self)
        self.server.bind("tcp://0.0.0.0:4242")
        print('server is start,wait connect...')
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

    manager = Manager(args.dataset,args.num,args.batch)
    manager.run()


