'''
    tree包的执行文件
'''
from .dtree import createTree,classify
import pandas as pd
import pickle
import random

# 特征标签
labels = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
              'marital-status', 'occupation',
              'relationship', 'race', 'sex', 'capital-gain', 'capital-loss', 'hours-per-week',
              'native-country']
# 特征的类型
labelType = ['continuous', 'uncontinuous', 'continuous',
                 'uncontinuous',
                 'continuous', 'uncontinuous',
                 'uncontinuous', 'uncontinuous', 'uncontinuous',
                 'uncontinuous', 'continuous', 'continuous',
                 'continuous', 'uncontinuous']

# 训练决策树
def train(dataset, labels, labelType):
    tree = createTree(dataset, labels, labelType)
    return tree

# 单个决策树的测试
def test(tree, testFilePath, labels, labelType, dataset):
    testDataset = pd.read_csv(testFilePath, header=None, sep=', ',engine='python')
    testDataset = testDataset[~testDataset.isin(['?']).any(axis=1)]
    testDataset = testDataset.values.tolist()
    total = len(testDataset)
    correct = 0
    error = 0
    i = 1
    for line in testDataset:
        print(i)
        result = classify(tree, line, labels, labelType) + '.'
        if result == line[-1]:
            correct += 1
        else:
            print('{} is error;result:{},correct:{}'.format(line, result, line[-1]))
            error += 1
        i += 1
    print('load {} lines data'.format(total))
    print('Correct: {},Error: {},Accuracy: {}'.format(correct, error, correct / total))


# 随机森林测试
def forestTest(forest):
    testDataset = pd.read_csv('./adult/adult.test', header=None, sep=', ',engine='python')
    testDataset = testDataset[~testDataset.isin(['?']).any(axis=1)]
    testDataset = testDataset.values.tolist()
    correct = 0
    error = 0
    for i in range(len(testDataset)):
        c1 = 0
        c2 = 0
        for tree in forest:
            classLabel = classify(tree,testDataset[i],labels,labelType)+'.'
            if classLabel == '<=50K.':
                c1+=1
            else:
                c2+=1
        answer = '<=50K.' if c1 > c2 else '>50K.'
        if answer == testDataset[i][-1]:
            correct += 1
        else:
            error += 1
    print('Correct: {},Error: {},Accuracy: {}'.format(correct, error, correct / len(testDataset)))

# 创建随机采样的数据集
def createSampleDataset(filename,batchSize):
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

# 将决策树存储到本地
def storeTree(tree, fileName):
    f = open(fileName, 'wb')
    pickle.dump(tree, f)
    f.close()


# 从本地获取决策树
def getTree(fileName):
    f = open(fileName, 'rb')
    tree = pickle.load(f)
    f.close()
    return tree
