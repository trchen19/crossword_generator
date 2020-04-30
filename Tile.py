class InfoStructure: 
    def __init__(self, word, resultSize, openLstPos, acrossBool, wordLstPos):
        self.word = word
        self.resultSize = resultSize
        self.openLstPos = openLstPos
        self.acrossBool = acrossBool
        self.wordLstPos = wordLstPos
    
    '''
        Getters
    '''
    def get_word(self):
        return self.word

    def get_resultSize(self):
        return self.resultSize
    
    def get_openLstPos(self):
        return self.openLstPos

    def get_acrossBool(self):
        return self.acrossBool

    def get_wordLstPos(self):
        return self.wordLstPos

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