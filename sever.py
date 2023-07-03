import RPi.GPIO as GPIO
import time

servo_pin = 11
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50)
servo.start(0)

min_duty_cycle = 2.5
max_duty_cycle = 12.5
min_angle = 0.0
max_angle = 180.0

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

try:
    while True:
        target_angle = float(input("请输入目标角度（0-180）："))
        if target_angle < 0 or target_angle > 180:
            print("角度超出范围，请重新输入！")
            continue

        duty_cycle = map_value(target_angle, min_angle, max_angle, min_duty_cycle, max_duty_cycle)
        servo.ChangeDutyCycle(duty_cycle)  # 设置舵机角度

        time.sleep(0.5)  # 等待舵机转动到目标角度

except KeyboardInterrupt:
    pass

servo.stop()
GPIO.cleanup()
