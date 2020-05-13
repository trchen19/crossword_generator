import mysql.connector
from Tile import InfoStructure, Tile, WordPattern

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1919myserver",
    database="mydatabase"
)

mycursor = mydb.cursor()

def set_freedom(wordPatterns):
    for pattern in wordPatterns:
        patternLen = pattern.get_direction()
        #setting initial freedome values for all wordpatterns
        # Query appropriate DB table given patternLen --> save rowcount as pattern freedom score (i.e pattern[3])
        sql = "SELECT COUNT(*) FROM words_"+str(patternLen)
        mycursor.execute(sql)
        (freedom,_) = mycursor.fetchone()
        pattern.set_freedom(freedom)

def query_wordpattern(pattern, regex=None):
    patternLen = pattern.get_length()

    table = "word_" + str(patternLen)

    sql = "SELECT * FROM "+ table + " ORDER BY RAND() LIMIT 10"

    if regex is not None: 
        sql = "SELECT * FROM "+ table + " WHERE term REGEXP '"+ regex + "' ORDER BY RAND() LIMIT 10"
        
    try:
        mycursor.execute(sql)
    except:
        print("COULDN'T QUERY TABLE: " + table)

    return mycursor.fetchall()

def get_freedom(pattern, regex=None):
    patternLen = pattern.get_length()

    table = "word_" + str(patternLen)

    sql = "SELECT COUNT(*) FROM " + table

    if regex is not None: 
        sql = "SELECT * FROM "+ table + " WHERE term REGEXP '"+ regex + "'" 
        
    try:
        mycursor.execute(sql)
    except:
        print("COULDN'T QUERY TABLE: " + table)
    
    (freedom,_) = mycursor.fetchone()
    return freedom

def get_seed(wordPatterns, tileDict):
    # Find word pattern with the most intersections 
    most_intersect = 0
    most_idx = -1
    count = 0

    for pattern in wordPatterns:
        if pattern.get_freedom() == 0:
            print("THIS BOARD IS NOT ARC-CONSISTENT")
            return None, None

        numIntersection = 0
        patternLen = pattern.get_length()

        #count number of intersections 
        startLoc = pattern.get_startLoc()
        x = startLoc[0]
        y = startLoc[1]

        if pattern.get_direction() == "across":
            for i in range(patternLen):
                tile = tileDict[(x, y+i)]
                if tile.is_intersection():
                    numIntersection += 1
        else:
            for i in range(patternLen):
                tile = tileDict[(x+i, y)]
                if tile.is_intersection():
                    numIntersection += 1
        
        if numIntersection > most_intersect:
            most_intersect = numIntersection
            most_idx = count

        count += 1

    pattern = wordPatterns[most_idx]
    results = query_wordpattern(pattern)
    return pattern, results

def get_ratio(start_x, start_y, direction, length, lst, tileDict):
    num_letters = 0
    if direction == "across":
        # Get instantiated tiles and letters
        for i in range(length):
            loc = (start_x, start_y+i)
            tile = tileDict[loc]
            if tile.get_tile_state():
                lst.append(tile.get_tile_letter()) 
                num_letters += 1
            else:
                lst.append(None)               
    else: 
        for i in range(length):
            loc = (start_x+i, start_y)
            tile = tileDict[loc]
            if tile.get_tile_state():
                lst.append(tile.get_tile_letter()) 
                num_letters += 1
            else:
                lst.append(None)           
    
        return num_letters/length

def build_regex(letter_lst):
    regex = ''
    count = 0
    for i in range(len(letter_lst)):
        if letter_lst[i] is not None:
            regex += '[a-zA-Z0-9]{'+ str(count) +'}'+letter_lst[i] + '{1}'
            count = 0
        elif i == len(letter_lst)-1 and letter_lst[i] is None:
            regex += '[a-zA-Z0-9]{'+ str(count) +'}'
        else:
            count +=1
    return regex

def backtrack():
    pass 

def choose_wordpattern(wordPatterns, tileDict):
    # Implement most_constrained and ratio
    highest_ratio = 0
    highest_ratio_letters = []
    highest_ratio_wp_lst = []
    for pattern in wordPatterns:
        # Check for arc-consistency... Check if there's a pattern with a Freedom of 0 and back track if needed 
        if pattern.get_freedom() == 0: 
            backtrack()

        startLoc = pattern.get_startLoc()
        start_x = startLoc[0]
        start_y = startLoc[1]
        direction = pattern.get_direction()
        length = pattern.get_length()

        #build Regex 
        instantiated_lst = []
        ratio = get_ratio(start_x, start_y, direction, length, instantiated_lst, tileDict)

        # Keeps word pattern with the highest ratio (First encountered saved)
        if ratio > highest_ratio:
            highest_ratio = ratio
            highest_ratio_letters = [instantiated_lst]
            highest_ratio_wp_lst = [pattern]
        elif ratio == highest_ratio:
            highest_ratio_letters.append(instantiated_lst)
            highest_ratio_wp_lst.append(pattern)

    # Get Most Constrained (First encountered kept)
    most_constrained_wp = None
    most_contrained = None
    for wp in highest_ratio_wp_lst:
        # Check for lowest freedom value
        if most_contrained is None or wp.get_freedom() < most_contrained:
            most_constrained_wp = wp
            most_contrained = wp.get_freedom()
    
    # Build Regex for Querying most contrained pattern
    regex = build_regex(highest_ratio_letters[highest_ratio_wp_lst.index(most_constrained_wp)])

    results = query_wordpattern(most_constrained_wp, regex)

    return most_constrained_wp,results

def instantiate_wordpattern(word, pattern, results, tileDict, wordPatterns, intersectionDict, openList, closedDict):
    #implement pick strategy

    # Add results to openList 
    openList.append(results)

    # Create ClosedList object for 
    closedList = InfoStructure(word, len(results), len(openList)- 1, pattern)
    closedDict[word] = closedList

    # Set tiles with given word
    startLoc = pattern.get_startLoc()
    start_x = startLoc[0]
    start_y = startLoc[1]
    direction = pattern.get_direction()
    patternLen = pattern.get_length()

    if direction == "across":
        for i in range(patternLen):
            tile_loc = (start_x, start_y + i)
            tile = tileDict[tile_loc]
            if not tile.get_tile_state():
                tile.set_letter(word[i])
                tile.set_state(True)
                if tile.is_intersection():
                    wp_letters = []
                    intersect_wp = intersectionDict[tile_loc][1]
                    intersect_wp_loc= intersect_wp.get_startLoc()
                    intersect_dir = intersect_wp.get_direction()
                    intersect_len = intersect_wp.get_length()
                    _ = get_ratio(intersect_wp_loc[0], intersect_wp_loc[1], intersect_dir, intersect_len, wp_letters, tileDict)
                    regex = build_regex(wp_letters)
                    freedom = get_freedom(intersect_wp, regex)
                    intersect_wp.set_freedom(freedom)
    else:
        for i in range(patternLen):
            tile_loc = (start_x+i, start_y)
            tile = tileDict[tile_loc]
            if not tile.get_tile_state():
                tile.set_letter(word[i])
                tile.set_state(True)
                if tile.is_intersection():
                    wp_letters = []
                    intersect_wp = intersectionDict[tile_loc][0]
                    intersect_wp_loc= intersect_wp.get_startLoc()
                    intersect_dir = intersect_wp.get_direction()
                    intersect_len = intersect_wp.get_length()
                    _ = get_ratio(intersect_wp_loc[0], intersect_wp_loc[1], intersect_dir, intersect_len, wp_letters, tileDict)
                    regex = build_regex(wp_letters)
                    freedom = get_freedom(intersect_wp, regex)
                    intersect_wp.set_freedom(freedom)


    
    
    