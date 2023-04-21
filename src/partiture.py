class Partiture:
    def __init__(self, group_notes) -> None:
        self.partiture = self.sort_notes(group_notes)
        self.highest_note = self.get_highest_note()
        self.lowest_note = self.get_lowest_note()

    def sort_notes(self, group_notes):
        notes = []

        for note in group_notes:
            if len(note) == 1:
                notes.append(note[0])
            else:
                for n in note:
                    n.duration = "corxera"
                    notes.append(n)
        return notes

    def get_highest_note(self):
        highest_note = None
        for note_obj in self.partiture:
            if highest_note is None or note_obj.note_value < highest_note.note_value:
                highest_note = note_obj
        return highest_note.note

    def get_lowest_note(self):
        lowest_note = None
        for note_obj in self.partiture:
            if lowest_note is None or note_obj.note_value > lowest_note.note_value:
                lowest_note = note_obj
        return lowest_note.note
