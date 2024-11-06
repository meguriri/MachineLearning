'''
    tree包的执行文件
'''
from .dtree import createTree,classify
import pandas as pd
import pickle
import random

# 特征标签
labels = ['age', 'workclass', 'fnlwgt', 
          'education', 'education-num',
            'marital-status', 'occupation',
            'relationship', 'race', 
            'sex', 'capital-gain', 
            'capital-loss', 'hours-per-week',
            'native-country']
# 特征的类型
labelType = ['continuous', 'uncontinuous', 
            'continuous','uncontinuous',
            'continuous', 'uncontinuous',
            'uncontinuous', 'uncontinuous', 
            'uncontinuous','uncontinuous', 
            'continuous', 'continuous',
            'continuous', 'uncontinuous']

# 训练决策树
def train(dataset, labels, labelType):
    tree = createTree(dataset, labels, labelType)
    return tree

# 单个决策树的测试
def test(tree, testFilePath, labels, labelType, dataset):
    # 读取测试集
    testDataset = pd.read_csv(testFilePath, header=None, sep=', ',engine='python')
    testDataset = testDataset[~testDataset.isin(['?']).any(axis=1)]
    testDataset = testDataset.values.tolist()
    # 测试集的数据个数
    total = len(testDataset)
    # 正确与错误的个数
    correct = 0
    error = 0
    # 循环读取测试集的每一条测试数据
    for line in testDataset:
        # 通过决策树对数据进行分类
        result = classify(tree, line, labels, labelType) + '.'
        # 与测试集数据标签一致
        if result == line[-1]:
            correct += 1
        # 与测试集数据标签不一致
        else:
            print('{} is error;result:{},correct:{}'.format(line, result, line[-1]))
            error += 1
    # 输出正确错误个数，以及正确率
    print('Correct: {},Error: {},Accuracy: {:.2f}'.format(correct, error, correct / total*100))


# 随机森林测试
def forestTest(forest):
    # 读取测试集
    testDataset = pd.read_csv('./adult/adult.test', header=None, sep=', ',engine='python')
    testDataset = testDataset[~testDataset.isin(['?']).any(axis=1)]
    testDataset = testDataset.values.tolist()
    # 正确与错误的个数
    correct = 0
    error = 0
    # 循环读取测试集的每一条测试数据
    for i in range(len(testDataset)):
        # 记录每棵树的分类
        c1 = 0
        c2 = 0
        # 循环读取每一棵决策树
        for tree in forest:
            # 获取当前这棵树的分类
            classLabel = classify(tree,testDataset[i],labels,labelType)+'.'
            # 统计每种分类的个数
            if classLabel == '<=50K.':
                c1+=1
            else:
                c2+=1
        # 选择每棵树分类结果的众数作为随机森林的分类
        answer = '<=50K.' if c1 > c2 else '>50K.'
        # 与测试集数据标签一致
        if answer == testDataset[i][-1]:
            correct += 1
        # 与测试集数据标签不一致
        else:
            error += 1
    # 输出正确错误个数，以及正确率
    print('Correct: {},Error: {},Accuracy: {:.2f}'.format(correct, error, correct / len(testDataset)*100))

# 创建随机采样的数据集
def createSampleDataset(filename,batchSize):
    # 指定随机选取多少个特征
    random_numbers = random.sample(range(0, len(labelType)), 5)
    # 读取数据集
    dataset = pd.read_csv(filename, header=None, sep=', ',engine='python')
    # 清洗数据
    dataset = dataset[~dataset.isin(['?']).any(axis=1)]
    # 随机选取n条数据作为训练集
    dataset = dataset.sample(n=batchSize)
    dataset = dataset.values.tolist()
    sampleDataset = [[row[i] for i in random_numbers] for row in dataset]
    # 将分类标签加入数据集
    for i in range(len(sampleDataset)):
        sampleDataset[i].append(dataset[i][-1])
    # 记录选择的特征标签和特征标签类型
    sampleLabels = []
    sampleLabelType = []
    for i in random_numbers:
        sampleLabels.append(labels[i])
        sampleLabelType.append(labelType[i])
    # 返回数据集和数特征标签
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
