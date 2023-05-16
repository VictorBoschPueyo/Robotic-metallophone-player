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

    def data_distance(self, pos):
        if pos < 10:
            return "0" + str(pos)
        else:
            return str(pos)

    def send_instructions(self, chain):
        last_left_pos = 8
        last_right_pos = 16
        
        self.write("L08WR16W")
        time.sleep(2)
        print("START PLAYING")

        for move in chain:
            # If the movement is a press and the motor is not in the correct position, move the motor and play the note
            # -- If the motor is in the correct position, don't move it, just play the note
            # If the movement is a transition and the motor is not in the correct position, move the motor

            # Instructions to move the motors
            # -- LXXP: Move the left motor to the position XX and play the note
            # -- LXXW: Move the left motor to the position XX and don't play the note
            # -- LWWW: Left wait
            # -- RXXP: Move the right motor to the position XX and play the note
            # -- RXXW: Move the right motor to the position XX and don't play the note
            # -- RWWW: Right wait

            start = time.time()
            data = ""

            if move[0] != None:
                if move[0].option == "P":
                    if (last_left_pos != move[0].note_pos):
                        data += "L" + self.data_distance(move[0].note_pos) + "P"
                        last_left_pos = move[0].note_pos
                    else:
                        data += "LWWP"
                else:
                    if (last_left_pos != move[0].note_pos):
                        data += "L" + self.data_distance(move[0].note_pos) + "W"
                        last_left_pos = move[0].note_pos
                    else:
                        data += "LWWW"
            else:
                data += "LWWW"

            if move[1] != None:
                if move[1].option == "P":
                    if (last_right_pos != move[1].note_pos):
                        data += "R" + self.data_distance(move[1].note_pos) + "P"
                        last_right_pos = move[1].note_pos

                    else:
                        data += "RWWP"
                else:
                    if (last_right_pos != move[1].note_pos):
                        data += "R" + self.data_distance(move[1].note_pos) + "W"
                        last_right_pos = move[1].note_pos
                    else:
                        data += "RWWW"
            else:
                data += "RWWW"

            if (time.time() - start) < 2:
                time.sleep(2 - (time.time() - start))

            if data != "LWWWRWWW":
                self.write(data)

        self.close()
        print("The partiture has been played!")
