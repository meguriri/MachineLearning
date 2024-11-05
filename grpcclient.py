import grpc
import pandas as pd
import proto.service_pb2
import proto.service_pb2_grpc
from tree import labels,labelType,train


def run():
  with grpc.insecure_channel('localhost:4243',options=(('grpc.enable_http_proxy', 0),)) as channel:
    stub = proto.service_pb2_grpc.ManagerStub(channel)
    while True:
      res = stub.GetDataSet(proto.service_pb2.GetDataSetRequest(id=1))
      # sampleDataset=res.data
      # sampleLabels=res.labels
      # sampleLabelType=res.labelType
      # if sampleDataset is None:
      #   break
      print('get dataset ok')
      # tree = train(sampleDataset,sampleLabels,sampleLabelType)
      print('train ok')
      tree ={"1":{"2":"ok","3":{"4":"ok","5":"unok","6":"unok"}}}
      res = stub.CommitTree(proto.service_pb2.CommitTreeRequest(tree=tree))
      del(tree)
      del(sampleDataset)
      if res.ok == False:
        break

if __name__ == "__main__":
  run()