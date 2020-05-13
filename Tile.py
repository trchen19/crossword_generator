class InfoStructure: 
    def __init__(self, word, resultSize, openLstPos, pattern):
        self.word = word
        self.resultSize = resultSize
        self.openLstPos = openLstPos
        self.pattern = pattern
    
    '''
        Getters
    '''
    def get_word(self):
        return self.word

    def get_resultSize(self):
        return self.resultSize
    
    def get_openLstPos(self):
        return self.openLstPos

    def get_pattern(self):
        return self.pattern

    ''''
        Setters
    ''' 

    def set_resultSize(self, size):
        self.resultSize = size

class Tile:
    def __init__(self, location, state, letter, intersection, clueNum):
        self.location = location
        self.state = state
        self.letter = letter
        self.intersection = intersection
        self.clueNum = clueNum

    ''''
        Getters
    ''' 

    def get_tile_location(self):
        return self.location

    def get_tile_state(self):
        return self.state

    def get_tile_letter(self):
        return self.letter
    
    def is_intersection(self):
        return self.intersection
    
    def get_tile_clue(self):
        return self.clueNum

    ''''
        Setters
    ''' 

    def set_letter(self, l):
        self.letter = l

    def set_state(self, bool):
        self.state = bool
        
    '''
        Helper Func for Debugging
    '''
    def print_tileInfo(self):
        print("Location: " + str(self.location))
        print("State: " + str(self.state))
        print("Letter: " + str(self.letter))
        print("Intersection: " + str(self.intersection))
        print("Clue Number: " + str(self.clueNum))
        print("-------------------------------------------")

class WordPattern:
    def __init__(self, startLoc, direction, length, freedom):
        self.startLoc = startLoc
        self.direction = direction
        self.length = length
        self.freedom = freedom 

    '''
        Getters
    '''
    def get_startLoc(self):
        return self.startLoc

    def get_direction(self):
        return self.direction

    def get_length(self):
        return self.length
    
    def get_freedom(self):
        return self.freedom

    '''
        Setters
    '''
    def set_startLoc(self, x, y):
        self.startLoc = (x, y)

    def set_direction(self, direction):
        self.direction = direction

    def set_length(self, length):
        self.length = length
    
    def set_freedom(self, freedom):
        self.freedom = freedom

    '''
        Debugging Print
    '''

    def print_pattern(self):
        print("starting location: " + str(self.startLoc))
        print("direction: " + self.direction)
        print("length: " + str(self.length))
        print("freedom: " + str(self.freedom))
        print()