import pigpio
import asyncio
import websockets

# 从文件或命令行参数加载配置
config = {
    "servo_pin_1": 11,  # 第一个舵机的 BCM GPIO 引脚号（-90 到 90 度）
    "servo_pin_2": 8,   # 第二个舵机的 BCM GPIO 引脚号（0 到 90 度）
    "websocket_server_address": "ws://node.ljcljc.cn:8110"
}

# 初始化 pigpio 库
pi = pigpio.pi()

# 设置初始舵机位置
pi.set_servo_pulsewidth(config["servo_pin_1"], 0)
pi.set_servo_pulsewidth(config["servo_pin_2"], 0)

async def control_servos():
    async with websockets.connect(config["websocket_server_address"]) as websocket:
        while True:
            try:
                # 提示客户端发送舵机1的角度
                await websocket.send("请发送舵机1的角度")

                # 接收舵机1的角度数据并验证范围
                while True:
                    angle_data = await websocket.recv()
                    angle_1 = float(angle_data)

                    if angle_1 >= -90 and angle_1 <= 90:
                        break
                    else:
                        await websocket.send("舵机1的角度无效，请重新发送")

                # 计算舵机1的脉冲宽度
                pulse_width_1 = 10.78 * angle_1 + 1547.4

                # 设置舵机1的位置
                pi.set_servo_pulsewidth(config["servo_pin_1"], pulse_width_1)

                # 提示客户端发送舵机2的角度
                await websocket.send("请发送舵机2的角度")

                # 接收舵机2的角度数据并验证范围
                while True:
                    angle_data = await websocket.recv()
                    angle_2 = float(angle_data)

                    if angle_2 >= 0 and angle_2 <= 90:
                        break
                    else:
                        await websocket.send("舵机2的角度无效，请重新发送")

                # 计算舵机2的脉冲宽度
                pulse_width_2 = 10.78 * angle_2 + 1547.4

                # 设置舵机2的位置
                pi.set_servo_pulsewidth(config["servo_pin_2"], pulse_width_2)

            except websockets.exceptions.ConnectionClosedOK:
                print("WebSocket 连接已关闭")
                break
            except Exception as e:
                print(f"发生错误: {e}")

# 启动舵机控制任务
asyncio.run(control_servos())

# 停止舵机运行
pi.set_servo_pulsewidth(config["servo_pin_1"], 0)
pi.set_servo_pulsewidth(config["servo_pin_2"], 0)

# 清理 pigpio 资源
pi.stop()
