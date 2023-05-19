from constants import *


class Key:
    def __init__(self, note) -> None:
        self.note = note
        self.motor = None
        self.weight_left = 0.0
        self.weight_right = 0.0


class Keyboard:
    def __init__(self, partiture) -> None:
        self.keyboard = self.create_keyboard(
            partiture.lowest_note, partiture.highest_note)

        self.notes = partiture.partiture

        self.n_keys = len(self.keyboard)
        self.middle = self.calculate_middle(partiture)

        self.pos_motor_left = 0
        self.pos_motor_right = self.n_keys - 1

        self.initial_calculation()

    def get_note_position(self, note):
        for i, key in enumerate(self.keyboard):
            if note in key.note:
                return i

    def create_keyboard(self, lowest_note, highest_note):
        keyboard = []
        ind_init = get_note_index(lowest_note)
        ind_end = get_note_index(highest_note)

        for i in range(ind_init, ind_end+1):
            keyboard.append(Key(entire_keyboard[i]))

        return keyboard

    def calculate_middle(self, partiture):
        # Sort partiture notes by note value
        notes = sorted(partiture.partiture, key=lambda x: x.note_value)

        # Get the middle note
        mid = len(notes)//2
        middle_note = notes[mid]

        return self.get_note_position(middle_note.note)

    def calculate_weights_left(self):
        for i in range(self.n_keys):
            if i < self.pos_motor_right:
                if i <= self.pos_motor_left:
                    self.keyboard[i].weight_left = 0.0
                else:
                    if i < self.middle:
                        self.keyboard[i].weight_left = abs(
                            self.pos_motor_left - i) * 0.05
                    elif i == self.middle:
                        self.keyboard[i].weight_left = 0.5
                    else:
                        self.keyboard[i].weight_left = abs(
                            self.pos_motor_left - i) * 0.1 + 0.5
            else:
                self.keyboard[i].weight_left = 999.9

    def calculate_weights_right(self):
        for i in range(self.n_keys):
            if i > self.pos_motor_left:
                if i >= self.pos_motor_right:
                    self.keyboard[i].weight_right = 0.0
                else:
                    if i > self.middle:
                        self.keyboard[i].weight_right = abs(
                            self.pos_motor_right - i) * 0.05
                    elif i == self.middle:
                        self.keyboard[i].weight_right = 0.5
                    else:
                        self.keyboard[i].weight_right = abs(
                            self.pos_motor_right - i) * 0.1 + 0.5
            else:
                self.keyboard[i].weight_right = 999.9

    def initial_calculation(self):
        # Position motors to the middle of "their" middle keyboard
        self.pos_motor_left = int(self.middle/2)
        self.pos_motor_right = int(self.middle + (self.n_keys - self.middle)/2)

        self.keyboard[self.pos_motor_left].motor = "left"
        self.keyboard[self.pos_motor_right].motor = "right"

        # Calculate weights
        self.calculate_weights_left()
        self.calculate_weights_right()

    def distribuite_movements(self):
        movements = []
        n_left = 0
        n_right = 0

        # Distribuite movements
        for note in self.notes:
            ind_note = self.get_note_position(note.note)

            if self.keyboard[ind_note].weight_left < self.keyboard[ind_note].weight_right:
                # Move motor left
                self.keyboard[self.pos_motor_left].motor = None
                self.keyboard[ind_note].motor = "left"
                self.pos_motor_left = ind_note
                movements.append(["L", note])
                n_left += 1
            elif self.keyboard[ind_note].weight_left == self.keyboard[ind_note].weight_right:
                # Move the motor that is closest to the middle
                if abs(self.pos_motor_left - self.middle) < abs(self.pos_motor_right - self.middle):
                    # Move motor left
                    self.keyboard[self.pos_motor_left].motor = None
                    self.keyboard[ind_note].motor = "left"
                    self.pos_motor_left = ind_note
                    movements.append(["L", note])
                    n_left += 1
                else:
                    # Move motor right
                    self.keyboard[self.pos_motor_right].motor = None
                    self.keyboard[ind_note].motor = "right"
                    self.pos_motor_right = ind_note
                    movements.append(["R", note])
                    n_right += 1
            else:
                # Move motor right
                self.keyboard[self.pos_motor_right].motor = None
                self.keyboard[ind_note].motor = "right"
                self.pos_motor_right = ind_note
                movements.append(["R", note])
                n_right += 1

            # Calculate weights
            self.calculate_weights_left()
            self.calculate_weights_right()

            self.print_keyboard()

        print("Left notes: " + str(n_left))
        print("Right notes: " + str(n_right))
        return movements
    

    def print_keyboard(self):
        divider = "+-------"*self.n_keys + "+"
        empty_row = "|       "*self.n_keys + "|"
        notes = ""
        motor = ""
        weights_left = ""
        weights_right = ""

        for key in self.keyboard:
            if len(key.note) == 2:
                notes += "|  " + key.note[0] + "  "
            else:
                notes += "|  " + key.note[0] + "   "

            if key.motor != None:
                motor += "| motor "
            else:
                motor += "|       "

            weights_left += "| " + \
                str(round(key.weight_left, 2)) + \
                (6 - len(str(round(key.weight_left, 2))))*" "
            weights_right += "| " + \
                str(round(key.weight_right, 2)) + \
                (6 - len(str(round(key.weight_right, 2))))*" "

        print(divider)
        print(empty_row)
        print(notes + "|")
        print(empty_row)
        print(motor + "|")
        print(empty_row)
        print(weights_left + "|")
        print(weights_right + "|")
        print(divider)
