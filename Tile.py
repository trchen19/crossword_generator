class QueryStructure: 
    def __init__(self, pattern, results):
        self.results = results
        self.pattern = pattern
    
    '''
        Getters
    '''
    def get_pattern(self):
        return self.pattern
        
    def get_resultSize(self):
        return len(self.results)
    
    def get_results(self):
        return self.results

    ''''
        Setters
    ''' 

    def set_results(self, results):
        self.result = results

    def print_info(self):
        print(self.results)
        print(self.pattern.print_pattern())
        
class Tile:
    def __init__(self, location, state, letter, intersection, clueNum):
        self.location = location
        self.state = state
        self.letter = letter
        self.intersection = intersection
        self.clueNum = clueNum
        self.user_letter = None

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

    def get_user_letter(self):
        return self.user_letter

    ''''
        Setters
    ''' 

    def set_letter(self, l):
        self.letter = l

    def set_state(self, bool):
        self.state = bool

    def set_user_letter(self, s):
        self.user_letter = s
        
    '''
        Method for Answer Checking 
    '''
    def compare_answer(self):
        if self.user_letter is None:
            return False
        return self.user_letter.lower() == self.letter.lower()
    
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
    def __init__(self, startLoc, direction, length, freedom, clueNum=None, clue=None, instantiated=False):
        self.startLoc = startLoc
        self.direction = direction
        self.length = length
        self.freedom = freedom 
        self.instantiated = instantiated
        self.clueNum = clueNum
        self.clue = clue
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

    def get_clueNum(self):
        return self.clueNum

    def get_clue(self):
        return self.clue

    def is_instantiated(self):
        return self.instantiated
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
    
    def set_clueNum(self, clueNum):
        self.clueNum = clueNum

    def set_clue(self, clue):
        self.clue = clue

    def set_instantiated(self, b):
        self.instantiated = b

    def is_equal(self, pattern):
        return self.startLoc == pattern.get_startLoc() and self.direction == pattern.get_direction()
    '''
        Debugging Print
    '''

    def print_pattern(self):
        print("starting location: " + str(self.startLoc))
        print("direction: " + self.direction)
        print("length: " + str(self.length))
        print("freedom: " + str(self.freedom))
        print("CLUENUM: " + str(self.clueNum) )
        print("CLUE: " + str(self.clue) )
        print()
