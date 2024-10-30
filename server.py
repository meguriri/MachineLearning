import zerorpc
import pandas as pd

def createSampleDataset(filename):
    # with open(filename,'r') as csvfile:
        # dataset = [row.strip().split(', ') for row in csvfile.readlines()]
        # dataset = [[int(i) if i.isdigit() else i for i in row] for row in dataset]
        dataset = pd.read_csv(filename,header=None,sep=', ')
        dataset = dataset[~dataset.isin(['?']).any(axis=1)]  
        dataset = dataset.sample(n=5000)
        dataset = dataset.values.tolist()
        # dataset = [[int(i) if i.isdigit() else i for i in row] for row in dataset]
        # cleanDataset(dataset)
        # del(dataset[-1])
        labels=['age','workclass','fnlwgt','education','education-num',
                'marital-status','occupation',
                 'relationship','race','sex','capital-gain','capital-loss','hours-per-week',
                 'native-country']
        labelType = ['continuous', 'uncontinuous', 'continuous',
                      'uncontinuous',
                      'continuous', 'uncontinuous',
                      'uncontinuous', 'uncontinuous', 'uncontinuous',
                      'uncontinuous', 'continuous', 'continuous',
                      'continuous', 'uncontinuous']
        return dataset,labels,labelType

clientList = []
testList = []

def getAnswer():
    testDataset = pd.read_csv('./adult/adult.test',header=None,sep=', ')
    testDataset = testDataset[~testDataset.isin(['?']).any(axis=1)]  
    testDataset = testDataset.values.tolist()
    correct = 0 
    error = 0 
    for i in range(len(testDataset)):
        c1 = 0
        c2 = 0
        for j in range(len(testList)):
          if testList[j][i] == '<=50K.':
              c1+=1
          else:
              c2+=1
        answer = '<=50K.' if c1>c2 else '>50K.'
        if answer == testDataset[i][-1]:
            correct+=1
        else:
            error+=1
    print('Correct: {},Error: {},Accuracy: {}'.format(correct,error,correct/len(testDataset)))

class MyRPCServer:
   
    def hello(self, name):
        """远程调用的函数示例"""
        return f"Hello, {name}!"
    def getDataSet(self):
        dataset,labels,labelType = createSampleDataset('./adult/adult.data')
        return dataset,labels,labelType
    def commitTest(self,test):
        testList.append(test)
        print('get test',test)
        if len(testList) == 5:
             getAnswer()
        return True
    
 
# 创建RPC服务器
server = zerorpc.Server(MyRPCServer())
server.bind("tcp://0.0.0.0:4242")

# 启动服务器
server.run()