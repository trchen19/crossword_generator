import Board

def get_wordPatterns(tiling):
    # Find wordPatterns 
    d = len(tiling)

    #list of starting and ending locations of each word pattern
    #problem: how to determine end and beginning? across? Down?
    wordPatterns = []

    # find patterns in every row (i.e. across word patterns)
    for i in range(d):
        started = False
        patternLen = 0
        startLoc = None
        for j in range(d):
            if tiling[i][j] and not started:
                started = True
                patternLen = 1
                startLoc = (i,j)
            elif tiling[i][j] and started:
                patternLen += 1
            elif not tiling[i][j] and started:
                started = False
                patternLen = 0
            if patternLen != 1: 
                wordPatterns.append( (startLoc, (i, j) ) )
                startLoc = None

    # find patterns in every row (i.e. down word patterns)
    for j in range(d):
        started = False
        patternLen = 0
        startLoc = None
        for i in range(d):
            if tiling[i][j] and not started:
                started = True
                patternLen = 1
                startLoc = (i,j)
            elif tiling[i][j] and started:
                patternLen += 1
            elif not tiling[i][j] and started:
                started = False
                patternLen = 0
            if patternLen != 1: 
                wordPatterns.append( (startLoc, (i, j) ) )
                startLoc = None
    return wordPatterns

def get_Tiles(tiling):
    # Create list of tiles
    tileLst = []

    for i in range(d):
        for j in range(d):
            if tiling[i][j]:
                location = (i, j)
                #need to figure out if a tile is an intersection or not
                # tileLst.append(new Tile(location, False, None, ))
        
# list of all words being considered in queries
openList = []

# list containing (word, clue)
clue = []

def if __name__ == "__main__":
    wordPatterns = get_wordPatterns(tiling)