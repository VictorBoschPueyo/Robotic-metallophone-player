import serial
import time


class ArduinoComunication:
    def __init__(self, port, baudrate):
        self.port = port  # /dev/ttyUSB0
        self.baudrate = baudrate  # 9600
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        self.ser.reset_input_buffer()

    def write(self, data):
        self.ser.write(data.encode('utf-8'))
        print(data)

    def read(self):
        return self.ser.readline().decode('utf-8').rstrip()

    def close(self):
        self.ser.close()
        print("The connection has been closed!")

    def send_move_by_move(self, moves):

        self.write("L08WR16W")
        time.sleep(2)
        print("START PLAYING")

        for move in moves:
            if move != "LWWWRWWW":
                self.write(move)

            time.sleep(1)

        self.close()
        print("The partiture has been played!")

    def send_full_data(self, data):
        self.write(data)
        self.close()
        print("The partiture has been played!")
