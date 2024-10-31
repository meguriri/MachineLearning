import zerorpc
import pandas as pd
import argparse
import random
import threading
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
            classLabel = t.classify(tree,testDataset[i],labels,labelType)+'.'
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




if __name__ == '__main__':
    # print('hello')
    forest = []
    idx = 1
    for i in range(16):
        tree = t.getTree('./model/tree_'+str(idx))
        print('./model/tree_'+str(idx))
        forest.append(tree)
        idx+=1
        print(len(forest))
    # tree = t.getTree('./model/tree.txt')
    # forest.append(tree)
    forestTest(forest)
    