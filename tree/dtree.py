'''
    dtree.py
    C4.5决策树的构建等函数
'''
from math import log2
import operator
import pandas as pd


# 读取全部数据集
def createDataset(filename):
    # 读取数据集
    dataset = pd.read_csv(filename, header=None, sep=', ',engine='python')
    # 清洗数据集
    dataset = dataset[~dataset.isin(['?']).any(axis=1)]
    dataset = dataset.values.tolist()
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
    # 返回数据集
    return dataset, labels, labelType


# 计算信息熵
def calculateEnt(dataset):
    # 分类统计
    classCount = {}
    n = len(dataset)
    # 遍历数据集
    for vec in dataset:
        # 获取当前数据的分类
        classification = vec[-1]
        # 更新classCount
        if classification not in classCount.keys():
            classCount[classification] = 0
        classCount[classification] += 1
    # 计算信息熵
    ent = 0.0
    for key in classCount:
        # 当前分类的占比
        p = classCount[key] / n
        # 信息熵
        ent += -1 * (p * log2(p))
    # 返回信息熵
    return ent

# 通过离散型特征划分数据集
def splitDataset(dataset, labelIdx, value):
    newDataset = []
    # 遍历数据集
    for vec in dataset:
        # 当前数据的特征等于选择的特征
        if vec[labelIdx] == value:
            # 剔除掉当前特征
            tmp = vec[:labelIdx]
            tmp.extend(vec[labelIdx + 1:])
            # 将该数据加入新的数据集
            newDataset.append(tmp)
    # 返回划分后的数据集
    return newDataset

# 通过连续型特征划分数据集
def splitContinuousDataset(dataset, labelIdx, value):
    # 大于分割点的数据集
    biggerDataset = []
    # 小于等于分割点的数据集
    smallerDataset = []
    # 遍历数据集
    for vec in dataset:
        # 剔除掉当前特征
        tmp = vec[:labelIdx]
        tmp.extend(vec[labelIdx + 1:])
        # 如果当前特征值大于分割点
        if float(vec[labelIdx]) > value:
            # 当前数据加入大于分割点的数据集
            biggerDataset.append(tmp)
        # 如果当前特征值小于等于分割点
        else:
            # 当前数据加入小于等于分割点的数据集
            smallerDataset.append(tmp)
    # 返回两个划分后的新的数据集
    return biggerDataset, smallerDataset


# 计算离散型特征的信息增益比
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
    # 信息增益
    gain = ent - entc
    # 全是一个类别split = 1
    if iv == 0:
        iv = 1
    # 计算信息增益率
    gainRadio = gain / iv
    return gainRadio

# 计算连续型特征的信息增益比
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
        # 获取当前分割点后的划分的两个数据集
        biggerDataset, smallerDataset = splitContinuousDataset(dataset, labelIdx, splitPoint[i])
        Db = len(biggerDataset) / len(dataset)
        Ds = len(smallerDataset) / len(dataset)
        # 计算当前划分的信息增益
        entc += Db * calculateEnt(biggerDataset)
        entc += Ds * calculateEnt(smallerDataset)
        gain = ent - entc
        # 更新最优的划分点
        if gain > bestGain:
            bestGain = gain
            iv += -1 * (Db * log2(Db))
            iv += -1 * (Ds * log2(Ds))
            bestSplitPoint = splitPoint[i]
            # TODO(meguriri): 修正信息增益
            # 计算最优信息增益率
            bestGainRatio = (log2(len(valueList) - 1) / abs(len(dataset))) / iv
    # 返回最优信息增益率和最优分割点
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
    # 遍历分类列表
    for i in classList:
        if i not in classficationCount.keys():
            classficationCount[i] = 0
        classficationCount[i] += 1
    # 排序选择最多的分类作为当前叶子节点的分类
    sortedClassCount = sorted(dict2list(classficationCount), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# 选择当前分支的最优的特征
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
        # 当前的特征是离散的
        if labelType[featureIdx] == 'uncontinuous':
            # 计算当前特征的信息增益率
            gainRatio = calGainRatioUnContinuous(dataset, featureIdx, ent)
            # 更新最优的特征和信息增益率
            if gainRatio > bestGainRatio:
                bestGainRatio = gainRatio
                bestFeatureIdx = featureIdx
                isContinuous = False
         # 当前的特征是连续的
        else:
            # 计算当前特征的信息增益率和划分点
            gainRatio, splitPoint = calGainRatioContinuous(dataset, featureIdx, ent)
            # 更新最优的特征和信息增益率
            if gainRatio > bestGainRatio:
                bestGainRatio = gainRatio
                bestFeatureIdx = featureIdx
                bestSplitPoint = splitPoint
                isContinuous = True
    # 返回最优特征和最优划分点和该特征是离散的还是连续的
    return bestFeatureIdx, bestSplitPoint, isContinuous

# 构建C4.5决策树
def createTree(dataset, labels, labelType):
    # 递归出口
    # 构造叶子节点分类
    classificationList = [vex[-1] for vex in dataset]
    # 如果当前只有一种分类，结束递归。选择当前分类作为当前叶子节点的分类
    if classificationList.count(classificationList[0]) == len(classificationList):
        print('classificate is ok', classificationList[0])
        return classificationList[0]
    # 如果当前没有可以分类的特征
    if len(dataset[0]) == 1:
        # 选择出现最多的分类作为当前叶子节点的分类
        print('no features', majority(classificationList))
        return majority(classificationList)
    # 选择最优特征和划分点
    bestFeatureIdx, bestSplitPoint, isContinuous = chooseBestSplit(dataset, labelType)
    # 未选出（说明当前的分类全是一样的数据，信息增益为0）
    if bestFeatureIdx == -1:
        # 选择出现最多的分类作为当前叶子节点的分类
        return majority(classificationList)
    bestFeature = labels[bestFeatureIdx]
    print(bestFeature)
    tree = {bestFeature: {}}
    # 更新特征标签和特征类型列表
    del (labels[bestFeatureIdx])
    del (labelType[bestFeatureIdx])
    # 选择的特征是连续的
    if isContinuous:
        # 获取划分点划分的两个数据集
        biggerDataset, smallerDataset = splitContinuousDataset(dataset, bestFeatureIdx, bestSplitPoint)
        # 递归建树
        subLabels = labels[:]
        subLabelType = labelType[:]
        tree[bestFeature]['>' + str(bestSplitPoint)] = createTree(biggerDataset, subLabels, subLabelType)
        subLabels = labels[:]
        subLabelType = labelType[:]
        tree[bestFeature]['<=' + str(bestSplitPoint)] = createTree(smallerDataset, subLabels, subLabelType)
    # 选择的特征是离散的
    else:
        # 获取最优特征的全部种类
        featureList = [vex[bestFeatureIdx] for vex in dataset]
        uniqueFeature = set(featureList)
        # 对每个种类递归建树
        for feature in uniqueFeature:
            subLabels = labels[:]
            subLabelType = labelType[:]
            subDataset = splitDataset(dataset, bestFeatureIdx, feature)
            tree[bestFeature][feature] = createTree(subDataset, subLabels, subLabelType)
    # 返回决策树
    return tree


# 分类任务，在树上根据data的特征
def classify(tree, data, labels, labelType):
    # 获取树的第一个特征选择
    feature = list(tree.keys())[0]
    # 获取树的子节点
    dic = tree[feature]
    # 获取该特征对应的index
    featureIdx = labels.index(feature)
    # 初始化选择的分类
    classLabel = '<=50k'
    # 非连续特征
    if labelType[featureIdx] == 'uncontinuous':  
        # 获取当前特征值
        nowFeature = data[featureIdx]
        # 寻找分支
        for key in dic.keys():
            if key == nowFeature:
                # 非叶子结点
                if type(dic[key]).__name__ == 'dict':
                    classLabel = classify(dic[key], data, labels, labelType)
                # 叶子结点
                else:
                    classLabel = dic[key]
                break
    # 连续特征
    else:  
        # 获取当前特征值
        nowFeature = float(data[featureIdx])
        firstBranch = list(dic.keys())[0]
        splitPoint = ''
        # 获取当前的分割点数值
        if str(firstBranch).startswith('>'):
            splitPoint = firstBranch[1:]
        else:
            splitPoint = firstBranch[2:]
        # 特征值与当前的分割点比较
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
    # 返回类别           
    return classLabel