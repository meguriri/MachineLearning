num_nodes=100

for i in $(seq 1 $num_nodes); do 
    python3 server.py -d './adult/adult.data' -n $i -b 24000  &
    pid=$!  # 获取后台进程的PID
    wait $pid  # 等待当前进程完成
    echo "运行成功: 实例 $i 完成"
done

wait