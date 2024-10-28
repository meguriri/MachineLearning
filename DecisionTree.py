# %%
from math import log
import operator

# %%
#数据集
def createDataSet():
    dataset = [[0, 0, 0, 0, 'no'],#数据集
               [0, 0, 0, 1, 'no'],
               [0, 1, 0, 1, 'yes'],
               [0, 1, 1, 0, 'yes'],
               [0, 0, 0, 0, 'no'],
               [1, 0, 0, 0, 'no'],
               [1, 0, 0, 1, 'no'],
               [1, 1, 1, 1, 'yes'],
               [1, 0, 1, 2, 'yes'],
               [1, 0, 1, 2, 'yes'],
               [2, 0, 1, 2, 'yes'],
               [2, 0, 1, 1, 'yes'],
               [2, 1, 0, 1, 'yes'],
               [2, 1, 0, 2, 'yes'],
               [2, 0, 0, 0, 'no']]
    labels = ['年龄', '有工作', '有自己的房子', '信贷情况']#分类属性
    return dataset, labels  

# %%
#计算信息熵
def calShannonEnt(dataset):
  rows = len(dataset)
  labelCounts = {}
  #提取分类标签
  for vec in dataset:
    label = vec[-1]
    if label not in labelCounts.keys():
      labelCounts[label] = 0
    labelCounts[label] += 1
  shannonEnt = 0.0
  for key in labelCounts:
    p = labelCounts[key] / rows
    shannonEnt += -1*(p*log(p,2))
  return shannonEnt

# %%
#划分数据集
def splitDataset(dataset,axis,value):
  retDataset = []
  for vec in dataset:
    #去掉axis这一列
    if vec[axis] == value:
      reducedVec = vec[:axis]
      reducedVec.extend(vec[axis+1:])
      retDataset.append(reducedVec)
  return retDataset

# %%
#选择最优特征
def chooseBestFeatureToSplit(dataset):
  numFeatures = len(dataset[0]) - 1
  baseEnt = calShannonEnt(dataset)
  print("dataset的信息熵",format(baseEnt,'.3f'))
  bestGain = 0.0
  bestFeature = -1
  for i in range(numFeatures):
    #提取第i个特征的所有类别
    featureList = [example[i] for example in dataset]
    featureSet = set(featureList)
    ent = 0.0
    for val in featureSet:
      subDataset = splitDataset(dataset,i,val)
      D = len(subDataset) / len(dataset)
      ent += D*calShannonEnt(subDataset)
    gain = baseEnt - ent 
    print(labels[i],"的信息增益",format(gain,'.3f'))
    if gain > bestGain:
      bestGain = gain
      bestFeature = i
  return bestFeature


# %%
#统计list中出现最多的分类
def majorityCnt(classList):
  classCount = {}
  for v in classList:
    if v not in classCount.keys():
      classCount[v] = 0
    classCount += 1
  sortedClassCount = sorted(classCount.items,key=operator.itemgetter(1),reverse=True) 
  return sortedClassCount[0][0]

# %%
#递归构建决策树
def createTree(dataset,labels,featureLabels):
  #获取全部数据的分类标签
  classList = [example[-1] for example in dataset]
  #数据的分类完全相同
  if classList.count(classList[0]) == len(classList):
    return classList[0]
  #遍历完所有特征后返回出现次数最多的分类标签
  if len(dataset[0])==1:
    return majorityCnt(classList)
  #获得信息增量最大的特征标签
  bestFeature = chooseBestFeatureToSplit(dataset)
  bestFeatureLabel = labels[bestFeature]
  print('最优的特征',bestFeatureLabel)
  #
  featureLabels.append(bestFeatureLabel)
  #建树
  tree = {bestFeatureLabel:{}}
  #删除最优特征标签
  del(labels[bestFeature])
  #获取最优特征标签的类别的集合
  featureValues = [example[bestFeature] for example in dataset]
  featureSet = set(featureValues)
  for val in featureSet:
    newLabels = labels[:]
    print(val)
    tree[bestFeatureLabel][val] = createTree(splitDataset(dataset,bestFeature,val),newLabels,featureLabels)
  return tree  


# %%
dataset,labels = createDataSet()
featureLabels = []
tree = createTree(dataset,labels,featureLabels)

tree


