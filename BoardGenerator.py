class Board:
    def __init__(self, pattern):3
        self.pattern = pattern
        self.word_lst = []

class Tile:
    def __init__(self, location, intersection):
        self.location = location
        self.instantiated = False
        self.letter = None
        self.intersection = intersection
        self.clue_num = 0

    def set_instantiated(self, bool):
        self.instantiated = bool
    
    def get_instantiated(self):
        return self.instantiated

    def set_letter(self, letter):
        self.letter = letter
    
    def get_letter(self):
        return self.letter
    
    def set_clue_num(self, clue_num):
        self.instantiated = bool
    
    def get_clue_num(self):
        return self.clue_num
    
