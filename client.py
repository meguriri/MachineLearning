import zerorpc
import pandas as pd


# 创建RPC客户端
client = zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")  # 连接到服务器地址
 
# 调用远程函数
response = client.hello("Alice")
print(response)  # 输出：Hello, Alice!
