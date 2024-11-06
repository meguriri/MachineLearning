'''
    test.py
    测试随机森林的性能，读取生成的决策树，执行测试
'''
import argparse
from tree import forestTest
import tree as t

if __name__ == '__main__':
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser()
    # 添加命令行参数
    parser.add_argument('-n','--num', type=int, help='forest size', required=False,default=10)
    # 解析命令行参数
    args = parser.parse_args()

    forest = []
    for i in range(args.num):
        print('./forest/tree_'+str(i))
        tree = t.getTree('./forest/tree_'+str(i)+'.txt')
        forest.append(tree)

    forestTest(forest)
    