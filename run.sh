# 默认子节点个数
num_nodes=1

# 启动主节点
# python3 server.py -d './adult/adult.data' -n 10 -b 1000 &

# 获取主节点的进程ID
# server_pid=$!
# echo "主节点已启动，进程ID为 $server_pid"

# 运行同一个脚本 num_nodes 次
for i in $(seq 1 $num_nodes); do
    python3 client.py &
    pid=$!  # 获取后台进程的PID
    wait $pid  # 等待当前进程完成
    echo "运行成功: 实例 $i 完成"
done

wait
# 等待主节点完成（可选）
# 主动终止主节点（可选）
# kill $server_pid
# echo "主节点已完成并被关闭."