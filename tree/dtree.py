from math import log2
import operator
import pickle
import pandas as pd


def createDataset(filename):
    dataset = pd.read_csv(filename, header=None, sep=', ',engine='python')
    dataset = dataset[~dataset.isin(['?']).any(axis=1)]
    dataset = dataset.values.tolist()
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
    return dataset, labels, labelType



def calculateEnt(dataset):
    classCount = {}
    n = len(dataset)
    for vec in dataset:
        classification = vec[-1]
        if classification not in classCount.keys():
            classCount[classification] = 0
        classCount[classification] += 1
    ent = 0.0
    for key in classCount:
        p = classCount[key] / n
        ent += -1 * (p * log2(p))
    return ent

def splitDataset(dataset, labelIdx, value):
    newDataset = []
    for vec in dataset:
        if vec[labelIdx] == value:
            tmp = vec[:labelIdx]
            tmp.extend(vec[labelIdx + 1:])
            newDataset.append(tmp)
    return newDataset


def splitContinuousDataset(dataset, labelIdx, value):
    biggerDataset = []
    smallerDataset = []
    for vec in dataset:
        tmp = vec[:labelIdx]
        tmp.extend(vec[labelIdx + 1:])
        if float(vec[labelIdx]) > value:
            biggerDataset.append(tmp)
        else:
            smallerDataset.append(tmp)
    return biggerDataset, smallerDataset


def calGainRatioUnContinuous(dataset, labelIdx, ent):
    # 获取该特征的类别
    featureList = [vec[labelIdx] for vec in dataset]
    uniqueFeature = set(featureList)
    # 条件熵
    entc = 0.0
    # 特征分裂信息度量
    iv = 0.0
    # 计算条件熵和特征分裂信息度量
    for val in uniqueFeature:
        subDataset = splitDataset(dataset, labelIdx, val)
        D = len(subDataset) / len(dataset)
        iv += -1 * (D * log2(D))
        entc += D * calculateEnt(subDataset)
    gain = ent - entc
    # 全是一个类别split = 1
    if iv == 0:
        iv = 1
    # 计算gainRatio
    gainRadio = gain / iv
    return gainRadio


def calGainRatioContinuous(dataset, labelIdx, ent):
    # 获取该连续特征的各种值
    valueList = [float(vec[labelIdx]) for vec in dataset]
    valueList = set(valueList)
    sortedValue = sorted(valueList)
    # 获取n-1个分割点
    splitPoint = []
    for i in range(len(sortedValue) - 1):
        splitPoint.append((sortedValue[i] + sortedValue[i + 1]) / 2.0)
    # 寻找最优分割点(信息增益最大)
    bestGainRatio = 0.0
    bestGain = 0.0
    bestSplitPoint = 0.0
    for i in range(len(splitPoint)):
        entc = 0.0
        iv = 0.0
        biggerDataset, smallerDataset = splitContinuousDataset(dataset, labelIdx, splitPoint[i])
        Db = len(biggerDataset) / len(dataset)
        Ds = len(smallerDataset) / len(dataset)
        entc += Db * calculateEnt(biggerDataset)
        entc += Ds * calculateEnt(smallerDataset)
        gain = ent - entc
        if gain > bestGain:
            bestGain = gain
            iv += -1 * (Db * log2(Db))
            iv += -1 * (Ds * log2(Ds))
            bestSplitPoint = splitPoint[i]
            # TODO(meguriri): 修正信息增益
            # 计算最优信息增益率
            bestGainRatio = (log2(len(valueList) - 1) / abs(len(dataset))) / iv
    return bestGainRatio, bestSplitPoint


# 字典转换元组列表
def dict2list(dic: dict):
    keys = dic.keys()
    values = dic.values()
    lst = [(k, v) for k, v in zip(keys, values)]
    return lst


# 特征用完后，叶子节点未分类成功，选择出现次数最多的分类
def majority(classList):
    classficationCount = {}
    for i in classList:
        if i not in classficationCount.keys():
            classficationCount[i] = 0
        classficationCount[i] += 1
    sortedClassCount = sorted(dict2list(classficationCount), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def chooseBestSplit(dataset, labelType):
    # 选取的特征是否连续
    isContinuous = False
    # 数据集整体的信息熵
    ent = calculateEnt(dataset)
    bestFeatureIdx = -1
    bestGainRatio = 0.0
    bestSplitPoint = 0.0
    # 遍历特征
    for featureIdx in range(len(dataset[0]) - 1):
        if labelType[featureIdx] == 'uncontinuous':
            gainRatio = calGainRatioUnContinuous(dataset, featureIdx, ent)
            if gainRatio > bestGainRatio:
                bestGainRatio = gainRatio
                bestFeatureIdx = featureIdx
                isContinuous = False
        else:
            gainRatio, splitPoint = calGainRatioContinuous(dataset, featureIdx, ent)
            if gainRatio > bestGainRatio:
                bestGainRatio = gainRatio
                bestFeatureIdx = featureIdx
                bestSplitPoint = splitPoint
                isContinuous = True
    return bestFeatureIdx, bestSplitPoint, isContinuous


def createTree(dataset, labels, labelType):
    # 递归出口
    # 构造叶子节点分类
    classificationList = [vex[-1] for vex in dataset]
    if classificationList.count(classificationList[0]) == len(classificationList):
        print('classificate is ok', classificationList[0])
        return classificationList[0]
    if len(dataset[0]) == 1:
        print('no features', majority(classificationList))
        return majority(classificationList)
    bestFeatureIdx, bestSplitPoint, isContinuous = chooseBestSplit(dataset, labelType)
    if bestFeatureIdx == -1:  # gain等于0
        return majority(classificationList)
    bestFeature = labels[bestFeatureIdx]
    print(bestFeature)
    tree = {bestFeature: {}}
    del (labels[bestFeatureIdx])
    del (labelType[bestFeatureIdx])
    if isContinuous:
        biggerDataset, smallerDataset = splitContinuousDataset(dataset, bestFeatureIdx, bestSplitPoint)
        subLabels = labels[:]
        subLabelType = labelType[:]
        tree[bestFeature]['>' + str(bestSplitPoint)] = createTree(biggerDataset, subLabels, subLabelType)
        subLabels = labels[:]
        subLabelType = labelType[:]
        tree[bestFeature]['<=' + str(bestSplitPoint)] = createTree(smallerDataset, subLabels, subLabelType)
    else:
        # 获取最优特征的全部类别
        featureList = [vex[bestFeatureIdx] for vex in dataset]
        uniqueFeature = set(featureList)
        for feature in uniqueFeature:
            subLabels = labels[:]
            subLabelType = labelType[:]
            subDataset = splitDataset(dataset, bestFeatureIdx, feature)
            tree[bestFeature][feature] = createTree(subDataset, subLabels, subLabelType)

    return tree


# 分类任务，在树上根据data的特征
def classify(tree, data, labels, labelType):
    feature = list(tree.keys())[0]
    dic = tree[feature]
    featureIdx = labels.index(feature)
    classLabel = '<=50k'

    if labelType[featureIdx] == 'uncontinuous':  # 非连续特征
        nowFeature = data[featureIdx]
        for key in dic.keys():
            if key == nowFeature:
                # 非叶子结点
                if type(dic[key]).__name__ == 'dict':
                    classLabel = classify(dic[key], data, labels, labelType)
                # 叶子结点
                else:
                    classLabel = dic[key]
                break
    else:  # 连续特征
        nowFeature = float(data[featureIdx])
        firstBranch = list(dic.keys())[0]
        splitPoint = ''
        if str(firstBranch).startswith('>'):
            splitPoint = firstBranch[1:]
        else:
            splitPoint = firstBranch[2:]
        if nowFeature > float(splitPoint):
            # 非叶子结点
            if type(dic['>' + str(splitPoint)]).__name__ == 'dict':
                classLabel = classify(dic['>' + str(splitPoint)], data, labels, labelType)
            # 叶子结点
            else:
                classLabel = dic['>' + str(splitPoint)]
        else:
            # 非叶子结点
            if type(dic['<=' + str(splitPoint)]).__name__ == 'dict':
                classLabel = classify(dic['<=' + str(splitPoint)], data, labels, labelType)
            # 叶子结点
            else:
                classLabel = dic['<=' + str(splitPoint)]
    return classLabel