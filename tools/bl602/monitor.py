import serial
import time
import threading

# 串口配置
PORT = '/dev/ttyACM1'
BAUDRATE = 2000000
SERIAL_BYTESIZE = serial.EIGHTBITS
SERIAL_PARITY = serial.PARITY_NONE
SERIAL_STOPBITS = serial.STOPBITS_ONE
SERIAL_FLOWCONTROL = False

# 初始化串口
try:
    ser = serial.Serial(
        port=PORT,
        baudrate=BAUDRATE,
        bytesize=SERIAL_BYTESIZE,
        parity=SERIAL_PARITY,
        stopbits=SERIAL_STOPBITS,
        timeout=1,  # 可设置超时时间
        xonxoff=SERIAL_FLOWCONTROL
    )
    print("串口已打开")
except serial.SerialException as e:
    print(f"无法打开串口: {e}")
    exit()

def read_serial():
    """读取串口数据"""
    buffer = ""
    while True:
        if ser.in_waiting > 0:  # 检查是否有数据可读
            data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')  # 读取数据并解码
            buffer += data  # 将新数据添加到缓冲区

            while '\n' in buffer:  # 检查缓冲区中是否有换行符
                line, buffer = buffer.split('\n', 1)  # 拆分出完整的一行
                print(f"{line.strip()}")  # 输出接收到的行

def write_serial(data):
    """写入串口数据"""
    # 发送数据时，以换行符结尾
    ser.write((data + '\n').encode())  # 将字符串编码成字节并写入串口
    print(f"{data}")

if __name__ == "__main__":
    # 启动读取线程
    read_thread = threading.Thread(target=read_serial, daemon=True)
    read_thread.start()

    try:
        while True:
            # 从标准输入读取要发送的数据
            user_input = input()
            if user_input.lower() == 'exit':
                break
            write_serial(user_input)
    except KeyboardInterrupt:
        print("程序被用户中断")
    finally:
        ser.close()  # 关闭串口
        print("串口已关闭")
