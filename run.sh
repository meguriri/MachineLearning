# 默认子节点个数
num_nodes=1

# 运行同一个脚本 num_nodes 次
for i in $(seq 1 $num_nodes); do
    python3 client.py &
    pid=$!  # 获取后台进程的PID
    wait $pid  # 等待当前进程完成
    echo "运行成功: 实例 $i 完成"
done

wait