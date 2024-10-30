@echo off
set num_nodes=50

:: 启动主节点
::start /B python server.py -d "./adult/adult.data" -n 10 -b 1000
::set server_pid=%ERRORLEVEL%
::echo 主节点已启动，进程ID为 %server_pid%

:: 运行 client.py num_nodes 次
for /L %%i in (1, 1, %num_nodes%) do (
    start /B python client.py
    echo 运行成功: 实例 %%i 完成
)

:: 等待主节点完成
:: 主动终止主节点（可选）
:: taskkill /PID %server_pid%
:: echo 主节点已完成并被关闭.
