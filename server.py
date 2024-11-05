import zerorpc
import pandas as pd
import argparse
import random
import threading
from tree import labels,labelType,forestTest,storeTree,createSampleDataset
import tree as t





class Manager:
    def __init__(self,filePath,clientNum,batchSize):
        self.testList = []
        self.ok = 0
        self.filePath = filePath
        self.clientNum = clientNum
        self.lock = threading.Lock()
        self.batchSize = batchSize
        
        self.forest = []
        # self.dataLoaded = False
        # self.loadAndSplitData(self,filePath)

    def getDataSet(self):
        # with self.lock:
            if self.ok >= self.clientNum:
                return None,None,None
            dataset, labels, labelType = createSampleDataset(self.filePath,self.batchSize)
            return dataset, labels, labelType

    def commitTest(self, tree):#test
        # with self.lock:
            # self.testList.append(test)
            self.forest.append(tree)
            storeTree(tree,fileName="./forest/tree_"+str(self.ok)+'.txt')
            print('now ok:',self.ok)
            self.ok+=1
            # print('get test', test)
            if  self.ok > self.clientNum:
                return None
            if self.ok == self.clientNum:
                print('all tree is ok')
                # getAnswer(self.testList)
                forestTest(self.forest)
                # self.stop()

    def stop(self):    
        self.server.close()
        print('server is close')

    def run(self):
        self.server = zerorpc.Server(self)
        self.server.bind("tcp://192.168.12.196:4242")
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

    manager = Manager(args.dataset,args.num,args.batch)
    manager.run()


