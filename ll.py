import pigpio

# 连接到pigpiod守护进程
pi = pigpio.pi()

# 读取全部引脚状态
status = {}
for pin in range(28):  # 假设树莓派上有28个引脚
    status[pin] = pi.read(pin)

# 输出引脚状态
for pin, state in status.items():
    print("引脚 {} 状态: {}".format(pin, state))

# 断开与pigpiod守护进程的连接
pi.stop()
