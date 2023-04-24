import serial

class arduino_comunication:
        def __init__(self, port, baudrate):
            self.port = port         #  /dev/ttyUSB0
            self.baudrate = baudrate #  9600
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.ser.flush()
    
        def write(self, data):
            self.ser.write(data.encode('utf-8'))
    
        def read(self):
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').rstrip()
                return line
    
        def close(self):
            self.ser.close()
