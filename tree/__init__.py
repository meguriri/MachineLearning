from .dtree import createTree,classify
import pandas as pd

def train(dataset, labels, labelType):
    tree = createTree(dataset, labels, labelType)
    # print(tree)
    return tree

def newTest(tree, testFilePath, labels, labelType):
    testDataset = pd.read_csv(testFilePath, header=None, sep=', ',engine='python')
    testDataset = testDataset[~testDataset.isin(['?']).any(axis=1)]
    testDataset = testDataset.values.tolist()
    # cleanoutdata(dataset)
    # del(dataset[0])
    # del(dataset[-1])
    testList = []
    # clean(testDataset,dataset)
    total = len(testDataset)
    for line in testDataset:
        result = classify(tree, line, labels, labelType) + '.'
        testList.append(result)
    return testList
