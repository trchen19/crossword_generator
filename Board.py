class InfoStructure: 
    def __init__(self):

class Board:
    def __init__(self, tiling):
        # tiling is a 2d matrix, where each index i,j is either True or False representing a 
        # white or blacked out box in the crossword board
        self.tiling = tiling 
        self.tilingInfo = {}
        for i in range(len(tiling)):
            for j in range(len(i)):
                if tiling[i, j]:
                    self.tilingInfo[(i,j)] = {"state": False, "letter": None, 
                        "intersection": False, "clueNum": 0}

        #list of starting and ending locations of each word pattern
        #problem: how to determine end and beginning? across? Down?
        self.wordPatterns = []
        
        # list of all words being considered in queries
        self.openList = []

        self.closedList =[]

        # list containing (word, clue)
        self.clue = []