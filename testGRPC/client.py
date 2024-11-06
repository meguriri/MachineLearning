from __future__ import print_function

import logging

import grpc
from proto import model_pb2
from proto import model_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:10086') as channel:
        client = model_pb2_grpc.ManagerStub(channel)  # 客户端使用Stub类发送请求,参数为频道,为了绑定链接
        response = client.GetDataSet(model_pb2.GetDatasetRequest(id=1))
        print(response.data)
        print(response.labels)
        print(response.labelType)


if __name__ == '__main__':
    logging.basicConfig()
    run()

