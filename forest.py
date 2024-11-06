'''
    forest.py
    单机版的随机森林训练测试
'''
import argparse
from tree import forestTest,createSampleDataset
import tree as t

if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()
    # 添加命令行参数
    parser.add_argument('-d','--dataset', type=str, help='dataset filepath')
    parser.add_argument('-n','--num', type=int, help='Age of the user', required=False,default=10)
    parser.add_argument('-b','--batch', type=int, help='batch size',required=False,default=5000)
    # 解析命令行参数
    args = parser.parse_args()

    # 存储决策树的随机森林数组
    forest = []

    # 循环训练n棵决策树
    for i in range(args.num):
        # 获取数据集
        sampleDataset, sampleLabels, sampleLabelType = createSampleDataset(args.dataset,args.batch)
        nowLabels = sampleLabels[:]
        nowLabelType = sampleLabelType[:]
        print('start',i)
        # 训练
        tree = t.train(sampleDataset, nowLabels, nowLabelType)
        print('train ok',i)
        # 将决策树存储到本地
        t.storeTree(tree,'./forest/tree_'+str(i)+'.txt')
        # 讲决策树加入随机森林数组
        forest.append(tree)
        # 清除内存缓存
        del(tree)
        del(sampleDataset)  
         
    # 训练结束后执行测试
    forestTest(forest)
    