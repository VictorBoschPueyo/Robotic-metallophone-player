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

entire_keyboard.reverse()


def get_note_index(note):
    for i, key in enumerate(entire_keyboard):
        if note in key:
            return i
