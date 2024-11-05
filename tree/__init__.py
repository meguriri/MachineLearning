from .dtree import createTree,classify
import pandas as pd
import pickle
import random

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
    return tree

def test(tree, testFilePath, labels, labelType, dataset):
    testDataset = pd.read_csv(testFilePath, header=None, sep=', ',engine='python')
    testDataset = testDataset[~testDataset.isin(['?']).any(axis=1)]
    testDataset = testDataset.values.tolist()
    # clean(testDataset, dataset)
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

def storeTree(tree, fileName):
    f = open(fileName, 'wb')
    pickle.dump(tree, f)
    f.close()


def getTree(fileName):
    f = open(fileName, 'rb')
    tree = pickle.load(f)
    f.close()
    return tree
