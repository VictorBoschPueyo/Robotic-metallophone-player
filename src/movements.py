
class Move:
    def __init__(self, note, option) -> None:
        self.note = note.note
        self.option = option # T = transition, P = play
        self.in_position = False
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
        left_notes = [ i for i, move in enumerate(self.movement) if move[0] == "L" ]
        right_notes = [ i for i, move in enumerate(self.movement) if move[0] == "R" ]

        # Calculate movement chain for left motor
        movement_chain_left = []
        movement_chain_right = []
        ind_left = 0
        ind_right = 0
        for ind_move in len(self.movement):
            if ind_move == left_notes[ind_left]:
                # Move left motor
                mov = Move(self.movement[left_notes[ind_left]][1], "P")
                movement_chain_left.append(mov)
                ind_left += 1
                # Right motor waiting
                movement_chain_right.append(Move(self.movement[right_notes[ind_left]][1], "T"))

                for i in mov.duration:
                    if ind_left < len(left_notes):
                        movement_chain_left.append(Move(self.movement[left_notes[ind_left]][1], "T"))
                    else:
                        movement_chain_left.append(None)

                    if ind_right < len(right_notes):
                        movement_chain_right.append(Move(self.movement[right_notes[ind_left]][1], "T"))
                    else:
                        movement_chain_right.append(None)

            elif ind_move == right_notes[ind_right]:
                # Move right motor
                mov = Move(self.movement[right_notes[ind_right]][1], "P")
                movement_chain_right.append(mov)
                ind_right += 1
                # Left motor waiting
                movement_chain_left.append(Move(self.movement[left_notes[ind_right]][1], "T"))

                for i in mov.duration:
                    if ind_left < len(left_notes):
                        movement_chain_left.append(Move(self.movement[left_notes[ind_left]][1], "T"))
                    else:
                        movement_chain_left.append(None)

                    if ind_right < len(right_notes):
                        movement_chain_right.append(Move(self.movement[right_notes[ind_left]][1], "T"))
                    else:
                        movement_chain_right.append(None)
        
        return zip(movement_chain_left, movement_chain_right)


        


