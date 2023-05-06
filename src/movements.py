from constants import *


class Move:
    def __init__(self, note, option) -> None:
        self.note = note.note
        self.option = option  # T = transition, P = play
        self.in_position = False

        self.note_pos = get_note_index(self.note)
        self.duration = self.set_duration(note.duration)

    def set_duration(self, duration):
        if duration == "corxera":
            return 1
        elif duration == "negra":
            return 2
        elif duration == "blanca":
            return 4
        elif duration == "rodona":
            return 8


class Movement_chain:
    def __init__(self, movement) -> None:
        self.movement = movement
        self.movement_chain = self.calculate_movement_chain()

    def calculate_movement_chain(self):
        left_notes = [i for i, move in enumerate(
            self.movement) if move[0] == "L"]
        right_notes = [i for i, move in enumerate(
            self.movement) if move[0] == "R"]

        # Calculate movement chain for left motor
        movement_chain_left = []
        movement_chain_right = []
        ind_left = 0
        ind_right = 0
        for ind_move in range(len(self.movement)):
            if ind_move == left_notes[ind_left]:
                # Move left motor
                mov = Move(self.movement[left_notes[ind_left]][1], "P")
                movement_chain_left.append(mov)
                if ind_left < len(left_notes):
                    ind_left += 1
                # Right motor waiting
                if ind_right < len(right_notes):
                    movement_chain_right.append(
                        Move(self.movement[right_notes[ind_right]][1], "T"))
                else:
                    movement_chain_right.append(None)

                for i in range(mov.duration - 1):
                    if ind_left < len(left_notes):
                        movement_chain_left.append(
                            Move(self.movement[left_notes[ind_left]][1], "T"))
                    else:
                        movement_chain_left.append(None)

                    if ind_right < len(right_notes):
                        movement_chain_right.append(
                            Move(self.movement[right_notes[ind_right]][1], "T"))
                    else:
                        movement_chain_right.append(None)

            elif ind_move == right_notes[ind_right]:
                # Move right motor
                mov = Move(self.movement[right_notes[ind_right]][1], "P")
                movement_chain_right.append(mov)
                if ind_right < len(right_notes):
                    ind_right += 1
                # Left motor waiting
                if ind_left < len(left_notes):
                    movement_chain_left.append(
                        Move(self.movement[left_notes[ind_left]][1], "T"))
                else:
                    movement_chain_left.append(None)

                for i in range(mov.duration - 1):
                    if ind_left < len(left_notes):
                        movement_chain_left.append(
                            Move(self.movement[left_notes[ind_left]][1], "T"))
                    else:
                        movement_chain_left.append(None)

                    if ind_right < len(right_notes):
                        movement_chain_right.append(
                            Move(self.movement[right_notes[ind_right]][1], "T"))
                    else:
                        movement_chain_right.append(None)

        return list(zip(movement_chain_left, movement_chain_right))

    def prepare_data_to_send(self):
        # Prepare data to send to motors
        # -- At the moment no transition movements are sent
        data = []
        for move in self.movement_chain:
            if move[0] != None and move[0].option == "P":
                info = "L" + str(move[0].note_pos)
                data.append(info)
                continue
            if move[1] != None and move[1].option == "P":
                info = "R" + str(move[1].note_pos)
                data.append(info)
                continue
            if (move[0] != None and move[0].option == "T") and (move[1] != None and move[1].option == "T"):
                info = "WAIT"
                data.append(info)
        return data

    def print_partiture_movement(self):
        n_left = 0
        n_right = 0
        for move in self.movement_chain:
            if move[0] and move[0].option == "P":
                if move[0].duration == 1:
                    tipus = " corxera"
                elif move[0].duration == 2:
                    tipus = " negra"
                elif move[0].duration == 4:
                    tipus = " blanca"
                elif move[0].duration == 8:
                    tipus = " rodona"
                print("Note: " + move[0].note + tipus + " (with left)")
                n_left += 1
            if move[1] and move[1].option == "P":
                if move[1].duration == 1:
                    tipus = " corxera"
                elif move[1].duration == 2:
                    tipus = " negra"
                elif move[1].duration == 4:
                    tipus = " blanca"
                elif move[1].duration == 8:
                    tipus = " rodona"
                print("Note: " + move[1].note + tipus + " (with right)")
                n_right += 1
        print("Total notes with left: " + str(n_left))
        print("Total notes with right: " + str(n_right))

    def print_movement_chain(self):
        for i, move in enumerate(self.movement_chain):
            print("Move: " + str(i))
            if move[0] == None:
                print("Left: No more notes")
            else:
                print("Left: " + move[0].note + " " + move[0].option)
                print("--Position: " + str(move[0].note_pos))
            if move[1] == None:
                print("Right: No more notes")
            else:
                print("Right: " + move[1].note + " " + move[1].option)
                print("--Position: " + str(move[1].note_pos))
            print("------------------")
