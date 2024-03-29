note_step = 0.0625

notes_map = {
    -4: "g5",
    -3: "f5",
    -2: "e5",
    -1: "d5",
    0:  "c5",
    1:  "b4",
    2:  "a4",
    3:  "g4",
    4:  "f4",
    5:  "e4",
    6:  "d4",
    7:  "c4",
    8:  "b3",
    9:  "a3",
    10: "g3",
    11: "f3",
    12: "e3",
    13: "d3",
    14: "c3",
    15: "b2",
    16: "a2",
}


class Note:
    def __init__(self, rectangle_note, duration, rectangle_penta, sost_notes=[], bem_notes=[]):
        self.rec = rectangle_note

        # Calculates which note is it by comparing the note's rectangle relative position in the pentagram's rectangle
        middle = rectangle_note.y + (rectangle_note.h / 2.0)
        height = (middle - rectangle_penta.y) / rectangle_penta.h

        self.note_value = int(height/note_step + 0.5)
        self.note = notes_map[self.note_value]

        self.duration = duration

        if any(n for n in sost_notes if n.note[0] == self.note[0]):
            self.note += "#"
            self.note_value += 0.5
        if any(n for n in bem_notes if n.note[0] == self.note[0]):
            self.note += "b"
            self.note_value -= 0.5
