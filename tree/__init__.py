from .dtree import createTree,classify
import pandas as pd
import pickle

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

def train(dataset, labels, labelType):
    tree = createTree(dataset, labels, labelType)
    # print(tree)
    return tree

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

def newTest(tree, testFilePath, labels, labelType):
    testDataset = pd.read_csv(testFilePath, header=None, sep=', ',engine='python')
    testDataset = testDataset[~testDataset.isin(['?']).any(axis=1)]
    testDataset = testDataset.values.tolist()
    testList = []
    total = len(testDataset)
    for line in testDataset:
        result = classify(tree, line, labels, labelType) + '.'
        testList.append(result)
    return testList

def storeTree(tree, fileName):
    f = open(fileName, 'wb')
    pickle.dump(tree, f)
    f.close()


def getTree(fileName):
    f = open(fileName, 'rb')
    tree = pickle.load(f)
    f.close()
    return tree
