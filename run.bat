@echo off
set num_nodes=50


:: 运行 client.py num_nodes 次
for /L %%i in (1, 1, %num_nodes%) do (
    start /B python client.py
    echo 运行成功: 实例 %%i 完成
)

