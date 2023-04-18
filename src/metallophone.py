

entire_keyboard = [
    ["g5"],
    ["f5#", "g5b"],
    ["f5"],
    ["e5"],
    ["d5#", "e5b"],
    ["d5"],
    ["c5#", "d5b"],
    ["c5"],
    ["b4"],
    ["a4#", "b4b"],
    ["a4"],
    ["g4#", "a4b"],
    ["g4"],
    ["f4#", "g4b"],
    ["f4"],
    ["e4"],
    ["d4#", "e4b"],
    ["d4"],
    ["c4#", "d4b"],
    ["c4"],
    ["b3"],
    ["a3#", "b3b"],
    ["a3"],
    ["g3#", "a3b"],
    ["g3"],
    ["f3#", "g3b"],
    ["f3"],
    ["e3"],
    ["d3#", "e3b"],
    ["d3"],
    ["c3#", "d3b"],
    ["c3"],
    ["b2"],
    ["a2#", "b2b"],
    ["a2"]]


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

        self.n_notes = len(self.keyboard)
        self.pos_motor_left = 0
        self.pos_motor_right = self.n_notes - 1

        self.initial_calculation()

    def get_note_index(self, note):
        for i, key in enumerate(entire_keyboard):
            if note in key:
                return i

    def create_keyboard(self, lowest_note, highest_note):
        keyboard = []
        ind_init = self.get_note_index(lowest_note)
        ind_end = self.get_note_index(highest_note)

        for i in range(ind_init, ind_end+1):
            keyboard.append(Key(entire_keyboard[i]))

        return keyboard

    def calculate_weights_left(self):
        for i in range(self.n_notes):
            if i < self.pos_motor_right:
                if i < self.pos_motor_left:
                    self.keyboard[i].weight_left = 0.05
                elif i == self.pos_motor_left:
                    self.keyboard[i].weight_left = 0.0
                else:
                    if i < self.n_notes/2 - 0.5:
                        self.keyboard[i].weight_left = abs(
                            self.pos_motor_left - i) * 0.05
                    elif i == (self.n_notes/2 - 0.5):
                        self.keyboard[i].weight_left = 0.5
                    else:
                        self.keyboard[i].weight_left = abs(
                            self.pos_motor_left - i) * 0.1 + 0.5
            else:
                self.keyboard[i].weight_left = 999.9

    def calculate_weights_right(self):
        for i in range(self.n_notes):
            if i > self.pos_motor_left:
                if i > self.pos_motor_right:
                    self.keyboard[i].weight_right = 0.05
                elif i == self.pos_motor_right:
                    self.keyboard[i].weight_right = 0.0
                else:
                    if i > self.n_notes/2 - 0.5:
                        self.keyboard[i].weight_right = abs(
                            self.pos_motor_right - i) * 0.05
                    elif i == (self.n_notes/2 - 0.5):
                        self.keyboard[i].weight_right = 0.5
                    else:
                        self.keyboard[i].weight_right = abs(
                            self.pos_motor_right - i) * 0.1 + 0.5
            else:
                self.keyboard[i].weight_right = 999.9

    def initial_calculation(self):
        # Position motors to the middle of "their" middle keyboard
        self.pos_motor_left = int((self.n_notes/2)/2)
        self.pos_motor_right = int((self.n_notes/2)/2 + self.n_notes/2)

        self.keyboard[self.pos_motor_left].motor = "left"
        self.keyboard[self.pos_motor_right].motor = "right"

        # Calculate weights
        self.calculate_weights_left()
        self.calculate_weights_right()

    def print_keyboard(self):
        for key in self.keyboard:
            print(key.note, key.motor, key.weight_left, key.weight_right)
