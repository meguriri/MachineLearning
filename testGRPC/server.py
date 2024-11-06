from concurrent import futures
import logging

import grpc
from proto import model_pb2
from proto import model_pb2_grpc


class Manager(model_pb2_grpc.ManagerServicer):  # 这里对应test.proto第17行定义的服务
    def GetDataSet(self, request, context):  # 这里对应test.proto第18行定义的info接口
        # print(request.name, request.age)
        return model_pb2.GetDatasetResponse(data=[model_pb2.Rowdata(row=["1","2"]),model_pb2.Rowdata(row=["3","4","5"])],labels=["1","2"],labelType=["2","3"])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))  # 开启多线程
    model_pb2_grpc.add_ManagerServicer_to_server(Manager(), server)  # 注册本地服务
    server.add_insecure_port('[::]:10086')  # 指定端口以及IP
    # server.add_insecure_port('0.0.0.0:10086')# 指定端口以及IP
    server.start()  # 启动服务器 start()是非阻塞的, 将实例化一个新线程来处理请求
    server.wait_for_termination()  # 阻塞调用线程，直到服务器终止


if __name__ == '__main__':
    logging.basicConfig()
    serve()

