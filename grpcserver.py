from concurrent import futures
import grpc
import argparse
import proto.service_pb2
import proto.service_pb2_grpc
from tree import forestTest,storeTree,createSampleDataset

class Manager(proto.service_pb2_grpc.ManagerServicer):
  def __init__(self,filePath,clientNum,batchSize):
    self.ok = 0
    self.filePath = filePath
    self.clientNum = clientNum
    self.batchSize = batchSize
    self.forest = []

  def GetDataSet(self, request, context):
    if self.ok >= self.clientNum:
      return None,None,None
    dataset, labels, labelType = createSampleDataset(self.filePath,self.batchSize)
    return proto.service_pb2.GetDataSetResponse(dataset, labels, labelType)
  
  def CommitTree(self, request, context):
    if self.ok > self.clientNum:
      return proto.service_pb2.CommitTreeResponse(ok=False)
    self.forest.append(request.tree)
    storeTree(request.tree,fileName="./forest/tree_"+str(self.ok)+'.txt')
    print('now ok:',self.ok)
    self.ok+=1
    if self.ok == self.clientNum:
      print('all tree is ok')
      forestTest(self.forest)
     
       

def serve(dataset,num,batch):
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  proto.service_pb2_grpc.add_ManagerServicer_to_server(Manager(dataset,num,batch), server)
  server.add_insecure_port('[::]:4243')
  server.start()
  print('server is start,wait connect...')
  server.wait_for_termination()

if __name__ == "__main__":
  # 创建 ArgumentParser 对象
  parser = argparse.ArgumentParser()
  # 添加命令行参数
  parser.add_argument('-d','--dataset', type=str, help='dataset filepath')
  parser.add_argument('-n','--num', type=int, help='Age of the user', required=False,default=10)
  parser.add_argument('-b','--batch', type=int, help='batch size',required=False,default=5000)
  # 解析命令行参数
  args = parser.parse_args()
  
  serve(args.dataset,args.num,args.batch)