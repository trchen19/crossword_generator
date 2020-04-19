import Board

wordPatterns = []
acrossPatterns = []
downPatterns = []
    
# list of all words being considered in queries
openList = []

# list containing (word, clue)
clue = []


def get_wordPatterns(tiling):
    # Find wordPatterns 
    d = len(tiling)

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
                endLoc = (i, j)
                wordPatterns.append( (startLoc, endLoc ) )
                acrossPatterns.append( (startLoc, endLoc) )
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
                endLoc = (i, j)
                wordPatterns.append( (startLoc, endLoc ) )
                downPatterns.append( (startLoc, endLoc) )

                startLoc = None

def determine_intersection(i, j):
    in_across = False
    in_down = False
    # Check across patterns
    for startLoc, endLoc in acrossPatterns:
        x = startLoc[0]
        start_y = startLoc[1]
        end_y = endLoc[1]

        if i == x:
            if j >= start_y and j <= end_y:
                in_across = True
        else:
            continue 
    
    # Check down patterns
    for startLoc, endLoc in downPatterns:
        y = startLoc[1]
        start_x = startLoc[0]
        end_x = endLoc[0]

        if j == y:
            if i >= start_x and i <= end_x:
                in_down = True
        else:
            continue 
    
    return in_down and in_across

def get_clue(i, j, lastClue):
    for startLoc, _ in acrossPatterns:
        if (i,j) == startLoc:
            lastClue += 1
            return lastClue
    for startLoc, _ in downPatterns:
        if (i,j) == startLoc:
            lastClue += 1
            return lastClue
    

def get_Tiles(tiling):
    # Create list of tiles
    tileLst = []
    lastClue = 0
    for i in range(d):
        for j in range(d):
            if tiling[i][j]:
                location = (i, j)
                intersection = determine_intersection(i, j)
                clueNum = get_clue(i, j, lastClue)
                if clueNum > lastClue:
                    tileLst.append(Tile(location, False, None, interesection, clueNum))
                else: 
                    print("This tile does not start a word Pattern")
    return tileLst

def if __name__ == "__main__":
    get_wordPatterns()