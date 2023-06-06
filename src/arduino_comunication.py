import serial
import time

from src.functions import load_animation

class ArduinoComunication:
    def __init__(self, port, baudrate):
        self.port = port  # /dev/ttyUSB0
        self.baudrate = baudrate  # 9600
        #self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        #self.ser.reset_input_buffer()

    def write(self, data):
        #self.ser.write(data.encode('utf-8'))
        print("Instruction: ", data)

    def close(self):
        #self.ser.close()
        print("\nThe connection has been closed!")

    def send_move_by_move(self, moves):
        # Init the arduino
        self.write("L08WR16W")
        time.sleep(2)
        print("START PLAYING")

        # Send the data
        for move in moves:
            if move != "LWWWRWWW":
                self.write(move)

            time.sleep(1)

        self.close()

    def send_full_data(self, moves):
        # Init the arduino
        self.write("L08WR16W")
        time.sleep(2)

        # Add last move to go back to the initial position
        moves.append("L08WR16W")

        # Send the data every 40 moves
        i = 0
        tempo = 0.5
        while i < len(moves):
            if i + 40 < len(moves):
                data = "".join(moves[i:i+40])
                self.write(data)
                time.sleep(tempo * 40)
            else:
                data = "".join(moves[i:])
                self.write(data)
                time.sleep(tempo * (len(moves) - i))
            i += 40

        # Fancy wait
        load_animation(20)

        self.close()
