import serial
import time


class ArduinoComunication:
    def __init__(self, port, baudrate):
        self.port = port  # /dev/ttyUSB0
        self.baudrate = baudrate  # 9600
        '''self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        self.ser.flush()'''

    def write(self, data):
        # self.ser.write(data.encode('utf-8'))
        print(data)

    def read(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()
            return line

    def close(self):
        # self.ser.close()
        print("The connection has been closed!")

    def data_distance(self, pos):
        if pos < 10:
            return "0" + str(pos)
        else:
            return str(pos)

    def send_instructions(self, chain):
        last_left_pos = 0
        last_right_pos = 0

        for move in chain:
            # If the movement is a press and the motor is not in the correct position, move the motor and play the note
            # -- If the motor is in the correct position, don't move it, just play the note
            # If the movement is a transition and the motor is not in the correct position, move the motor

            # Instructions to move the motors
            # -- LPP: Play the note in the left motor
            # -- RPP: Play the note in the right motor
            # -- LXX: Move the left motor to the position XX
            # -- RXX: Move the right motor to the position XX
            # -- LWW: Do not move the left motor
            # -- RWW: Do not move the right motor

            data = ""

            if move[0] != None:
                if move[0].option == "P":
                    if (last_left_pos != move[0].note_pos):
                        self.write(
                            "L" + self.data_distance(move[0].note_pos) + "RWW")
                        last_left_pos = move[0].note_pos

                        '''while (self.read() != "FINISH"):
                            time.sleep(0.05)'''

                        data += "LPP"
                    else:
                        data += "LPP"
                else:
                    if (last_left_pos != move[0].note_pos):
                        data += "L" + self.data_distance(move[0].note_pos)
                        last_left_pos = move[0].note_pos
                    else:
                        data += "LWW"
            else:
                data += "LWW"

            if move[1] != None:
                if move[1].option == "P":
                    if (last_right_pos != move[1].note_pos):
                        self.write(
                            "LWW" + "R" + self.data_distance(move[1].note_pos))
                        last_right_pos = move[1].note_pos

                        '''while (self.read() != "FINISH"):
                            time.sleep(0.05)'''

                        data += "RPP"
                    else:
                        data += "RPP"
                else:
                    if (last_right_pos != move[1].note_pos):
                        data += "R" + self.data_distance(move[1].note_pos)
                        last_right_pos = move[1].note_pos
                    else:
                        data += "RWW"
            else:
                data += "RWW"

            self.write(data)

            time.sleep(0.5)

        self.close()
        print("The partiture has been played!")
