import serial
import time

from src.functions import load_animation

class ArduinoComunication:
    def __init__(self, port, baudrate):
        self.port = port  # /dev/ttyUSB0
        self.baudrate = baudrate  # 9600
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        self.ser.reset_input_buffer()
        self.tempo = 0.45

    def write(self, data):
        self.ser.write(data.encode('utf-8'))
        print("Instruction: ", data)

    def close(self):
        self.ser.close()
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

            time.sleep(self.tempo)

        self.close()

    def send_full_data(self, moves):
        # Init the arduino
        self.write("L08WR16W")
        time.sleep(2)

        # Add last move to go back to the initial position
        moves.append("L08WR16W")

        # Send the data every 40 moves
        i = 0
        while i < len(moves):
            if i + 40 < len(moves):
                data = "".join(moves[i:i+40])
                self.write(data)
                wait = self.tempo * 40
            else:
                data = "".join(moves[i:])
                self.write(data)
                wait = self.tempo * (len(moves) - i)
                
            # Fancy wait
            load_animation(wait)
            i += 40

        self.close()
