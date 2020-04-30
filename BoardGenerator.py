from Tile import Tile
debug = False

def get_wordPatterns(tiling):
    # Find wordPatterns 
    d = len(tiling)

    # list of tuples in form: (startLoc, direction, length, freedom)
    wordPatterns = []

    # find patterns in every across (i.e. across word patterns)

    for i in range(d):
        patternLen = 0
        startLoc = None
        freedom = -1
        for j in range(d):
            if debug:
                print("-----------------")
                print(i, j)
                print(tiling[i][j])
                print("len: " + str(patternLen))
                print("START: " + str(startLoc))
                
            if tiling[i][j] and patternLen == 0:
                patternLen = 1
                startLoc = (i,j)
            elif tiling[i][j] and patternLen > 0:
                patternLen += 1
            elif not tiling[i][j] and patternLen > 1:
                wordPatterns.append( (startLoc, "across", patternLen, freedom) )
                startLoc = None
                patternLen = 0
            else:
                startLoc = None
                patternLen = 0

            if j == d-1 and patternLen > 1:
                wordPatterns.append( (startLoc, "across", patternLen, freedom) )


    # find patterns in every down (i.e. down word patterns)
    for j in range(d):
        patternLen = 0
        startLoc = None
        freedom = 1
        for i in range(d):    
            if tiling[i][j] and patternLen == 0:
                patternLen = 1
                startLoc = (i,j)
            elif tiling[i][j] and patternLen > 0:
                patternLen += 1
            elif not tiling[i][j] and patternLen > 1:
                wordPatterns.append( (startLoc, "down", patternLen, freedom) )
                startLoc = None
                patternLen = 0
            else:
                startLoc = None
                patternLen = 0

            if i == d-1 and patternLen > 1:
                wordPatterns.append( (startLoc, "down", patternLen, freedom) )

    return wordPatterns

def determine_intersection(i, j, wpLst):
    in_across = False
    in_down = False

    for pattern in wpLst:
        startLoc = pattern[0]
        x = startLoc[0]
        y = startLoc[1]

        if pattern[1] == "across":
            end_y = y + pattern[2]
            if i == x:
                if j >= y and j <= end_y:
                    in_across = True
            else:
                continue     
        else:
            end_x = x + pattern[2]
            if j == y:
                if i >= x and i <= end_x:
                    in_down = True
            else:
                continue    
 
    return in_down and in_across

def get_clue(i, j, lastClue, wpLst):
    for pattern in wpLst:
        if (i,j) == pattern[0]:
            nextClue = lastClue + 1
            return nextClue
    return lastClue

def get_Tiles(tiling, wordPatterns):
    # Create list of tiles
    d = len(tiling)

    tileDict = {}
    lastClue = 0
    for i in range(d):
        for j in range(d):
            if tiling[i][j]:
                location = (i, j)
                intersection = determine_intersection(i, j, wordPatterns)
                clueNum = get_clue(i, j, lastClue, wordPatterns)
                if clueNum > lastClue:
                    t = Tile(location, False, None, intersection, clueNum)
                    tileDict[(i,j)] = t
                    lastClue = clueNum
                else: 
                    t = Tile(location, False, None, intersection, 0)
                    tileDict[(i,j)] = t
    return tileDict