import zerorpc
import pandas as pd
import argparse
import random
import threading
from tree import labels,labelType,forestTest
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

def createSampleDataset(filename,batchSize):
    random_numbers = random.sample(range(0, len(labelType)), 6)
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



if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()
    # 添加命令行参数
    parser.add_argument('-d','--dataset', type=str, help='dataset filepath')
    parser.add_argument('-n','--num', type=int, help='Age of the user', required=False,default=10)
    parser.add_argument('-b','--batch', type=int, help='batch size',required=False,default=5000)
    # 解析命令行参数
    args = parser.parse_args()

    forest = []
    for i in range(args.num):
        sampleDataset, sampleLabels, sampleLabelType = createSampleDataset(args.dataset,args.batch)
        nowLabels = sampleLabels[:]
        nowLabelType = sampleLabelType[:]
        print('start',i)
        tree = t.train(sampleDataset, nowLabels, nowLabelType)
        print('train ok',i)
        t.storeTree(tree,'./model/tree_'+str(i)+'.txt')
        forest.append(tree)
        del(tree)
        del(sampleDataset)   

    forestTest(forest)
    