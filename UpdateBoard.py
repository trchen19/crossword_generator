import mysql.connector
from Tile import QueryStructure, Tile, WordPattern
import BoardGenerator

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1919myserver",
    database="mydatabase"
)

mycursor = mydb.cursor()

DEBUG = False

def query_wordpattern(pattern, regex=None):
    patternLen = pattern.get_length()

    table = "words_" + str(patternLen)

    sql = "SELECT * FROM "+ table + " ORDER BY RAND() LIMIT 100"

    if regex is not None:
        sql = "SELECT * FROM "+ table + " WHERE term REGEXP '"+ regex + "' ORDER BY RAND() LIMIT 100"

    if DEBUG:
        print()
        print(regex)
        print(sql)

    try:
        mycursor.execute(sql)
        return mycursor.fetchall()
    except:
        print(regex)
        print("COULDN'T QUERY TABLE: " + table)

    return None

def set_freedom(wordPatterns):
    if DEBUG:
        print("SETTING FREEDOM")
    for pattern in wordPatterns:
        patternLen = pattern.get_length()
        #setting initial freedome values for all wordpatterns
        # Query appropriate DB table given patternLen --> save rowcount as pattern freedom score (i.e pattern[3])
        sql = "SELECT COUNT(*) FROM words_"+str(patternLen)
        mycursor.execute(sql)
        (freedom,) = mycursor.fetchone()
        pattern.set_freedom(freedom)

def get_freedom(pattern, regex=None):
    patternLen = pattern.get_length()

    table = "words_" + str(patternLen)

    sql = "SELECT COUNT(*) FROM " + table

    if DEBUG:
        print(regex)

    if regex is not None:
        sql = "SELECT COUNT(*) FROM "+ table + " WHERE term REGEXP '"+ regex + "'"

    try:
        mycursor.execute(sql)
        (freedom,) = mycursor.fetchone()
        if DEBUG:
            print("FREEDOM: " + str(freedom))
        return freedom
    except:
        print(regex)
        print("COULDN'T QUERY TABLE: " + table)

    return None


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

    if DEBUG:
        print("**************************")
        print("GETTING RATIO")
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
    if DEBUG:
        print("-----------------------")
        print("BUILDING REGEX")
        print(letter_lst)
    regex = ''
    count = 0
    for i in range(len(letter_lst)):
        if letter_lst[i] is not None:
            regex += '[a-zA-Z0-9]{'+ str(count) +'}'+letter_lst[i] + '{1}'
            count = 0
        elif i == len(letter_lst)-1 and letter_lst[i] is None:
            regex += '[a-zA-Z0-9]{'+ str(count+1) +'}'
        else:
            count +=1
    if DEBUG:
        print("BUILT: " + regex)
        print("-------------------------")
    return regex

def change_last_pattern(closedList, tileDict, intersectionDict, clues):
    if DEBUG:
        print("*-*-*-*-*-*-*-*-")
        print("CHANGING LAST PATTERN TO NEXT WORD")
        print("*-*-*-*-*-*-*-*-")
    # Change tiles to next word in the closedList results
    pattern = closedList.get_pattern()
    results = closedList.get_results()
    if DEBUG:
        print("OLD RESULTS: ")
        print(results)
    clues.remove(results[-1])
    results.remove(results[-1])

    if DEBUG:
        print("NEW RESULTS: ")
        print(results)

    in_clues = True
    while in_clues:
        if not results:
            if DEBUG:
                print("?!?!?!??!?!?!?!?!?!?!?!?!?")
                print("CLUE LIST")
                print("?!?!?!??!?!?!?!?!?!?!?!?!?")
                print(clues)
                print("CHANGE LAST PATTERN: all words used")
            return False

        (word, clue) = results[-1]
        if (word, clue) not in clues:
            clues.append((word, clue))
            in_clues = False
        else:
            results.remove((word, clue))

    closedList.set_results(results)
    word = results[-1][0]
    pattern.set_clue(results[-1][1])
    if DEBUG:
        print("NEW WORD: "+ word)
    # Set tiles with given word
    startLoc = pattern.get_startLoc()
    start_x = startLoc[0]
    start_y = startLoc[1]
    direction = pattern.get_direction()
    patternLen = pattern.get_length()
    if DEBUG:
        pattern.print_pattern()
    if direction == "across":
        for i in range(patternLen):
            tile_loc = (start_x, start_y + i)
            tile = tileDict[tile_loc]
            if tile.is_intersection():
                intersect_wp = intersectionDict[tile_loc][1]
                if not intersect_wp.is_instantiated():
                    if DEBUG:
                        print(word[i])
                    tile.set_letter(word[i])
                    tile.set_state(True)
                    wp_letters = []
                    intersect_wp_loc= intersect_wp.get_startLoc()
                    intersect_dir = intersect_wp.get_direction()
                    intersect_len = intersect_wp.get_length()
                    ratio = get_ratio(intersect_wp_loc[0], intersect_wp_loc[1], intersect_dir, intersect_len, wp_letters, tileDict)
                    regex = build_regex(wp_letters)
                    freedom = get_freedom(intersect_wp, regex)
                    intersect_wp.set_freedom(freedom)
                    if ratio == 1:
                        lst = query_wordpattern(intersect_wp, regex)
                        if lst:
                            _, c = lst[0]
                            intersect_wp.set_clue(c)
                        intersect_wp.set_instantiated(True)
            else:
                if DEBUG:
                    print(word[i])

                tile.set_letter(word[i])
                tile.set_state(True)
    else:
        for i in range(patternLen):
            tile_loc = (start_x+i, start_y)
            tile = tileDict[tile_loc]
            if tile.is_intersection():
                intersect_wp = intersectionDict[tile_loc][0]
                if not intersect_wp.is_instantiated():
                    tile.set_letter(word[i])
                    tile.set_state(True)
                    wp_letters = []
                    intersect_wp_loc= intersect_wp.get_startLoc()
                    intersect_dir = intersect_wp.get_direction()
                    intersect_len = intersect_wp.get_length()
                    ratio = get_ratio(intersect_wp_loc[0], intersect_wp_loc[1], intersect_dir, intersect_len, wp_letters, tileDict)
                    regex = build_regex(wp_letters)
                    freedom = get_freedom(intersect_wp, regex)
                    intersect_wp.set_freedom(freedom)
                    if ratio == 1:
                        lst = query_wordpattern(intersect_wp, regex)
                        if lst:
                            _, c = lst[0]
                            intersect_wp.set_clue(c)
                        intersect_wp.set_instantiated(True)
            else:
                tile.set_letter(word[i])
                tile.set_state(True)

    if DEBUG:
        print("*_*_*_*_*_*__*_*_*_*_*_*_*_*_*")

    return True

def backtrack(tileDict, intersectionDict, infoList, clues, backtrackCount):
    # Backtrack called when all results in the last closedList in infoList are used up
    # Get last pattern instantiated
    # Remove last closedList from infoList
    if DEBUG:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("BACKTRACKING")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("INFO-LIST LEN: " + str(len(infoList)))
    last_closedList = infoList.pop(-1)
    if DEBUG:
        print("INFO-LIST LEN AFTER POP: " + str(len(infoList)))
        print(last_closedList)
    last_pattern = last_closedList.get_pattern()
    if DEBUG:
        print(last_closedList.get_results())

    if last_closedList.get_results():
        if DEBUG:
            print("WORD REMOVED FROM CLUES")

        clues.remove(last_closedList.get_results()[-1])

    # Reset tiles that aren't intersection tiles and intersection tiles that aren't in previously instantiated patterns
    startLoc = last_pattern.get_startLoc()
    start_x = startLoc[0]
    start_y = startLoc[1]
    direction = last_pattern.get_direction()
    patternLen = last_pattern.get_length()
    last_pattern.set_clue(None)
    last_pattern.set_instantiated(False)
    backtrackCount += 1

    if direction == "across":
        for i in range(patternLen):
            tile_loc = (start_x, start_y + i)
            tile = tileDict[tile_loc]
            if tile.is_intersection():
                intersect_wp = intersectionDict[tile_loc][1]
                if not intersect_wp.is_instantiated():
                    tile.set_letter(None)
                    tile.set_state(False)
            else:
                tile.set_letter(None)
                tile.set_state(False)
    else:
        for i in range(patternLen):
            tile_loc = (start_x + i, start_y)
            tile = tileDict[tile_loc]
            if tile.is_intersection():
                intersect_wp = intersectionDict[tile_loc][0]
                if not intersect_wp.is_instantiated():
                    tile.set_letter(None)
                    tile.set_state(False)
            else:
                tile.set_letter(None)
                tile.set_state(False)

    # try different word from results in the new "last" closed List
    if infoList:
        if DEBUG:
            print("CALLING CHANGE LAST PATTERN FROM BACKTRACK")
        success = change_last_pattern(infoList[-1], tileDict, intersectionDict, clues)
        if DEBUG:
            print("NUM OF CLOSEDLISTS LEFT: " + str(len(infoList)))
        if not success:
            if DEBUG:

                print("RECURSIVE CALL")
            success, backtrackCount = backtrack(tileDict, intersectionDict, infoList, clues, backtrackCount)

        return success, backtrackCount
    else:
        print("INVALID BOARD")
        return False, backtrackCount


def choose_wordpattern(wordPatterns, tileDict, intersectionDict, infoList, clues, backtrackCount):
    if DEBUG:
        print("--------------------------------")
        print("CHOOSING WORDPATTERN")
        print("--------------------------------")
    # Implement most_constrained and ratio
    highest_ratio = -1
    highest_ratio_letters = []
    highest_ratio_wp_lst = []
    for pattern in wordPatterns:
        if DEBUG:
            print("PATTERN FREEDOM: " + str(pattern.get_freedom()))
        # Check for arc-consistency... Check if there's a pattern with a Freedom of 0 and back track if needed
        # First try a different word from the last closedList in infoList
        # If no more words in results from last closedList to try, BACKTRACK.
        if pattern.get_freedom() == 0:
            if DEBUG:
                print("NOT ARC-CONSISTENT...")
            last_closedList = infoList[-1]
            if DEBUG:
                last_closedList.print_info()
            if last_closedList.get_resultSize() > 1:
                if DEBUG:
                    print("Changing to next pattern")
                success = change_last_pattern(last_closedList, tileDict, intersectionDict, clues)
            else:
                if DEBUG:
                    print("Backtracking")
                success, backtrackCount = backtrack(tileDict, intersectionDict, infoList, clues, backtrackCount)
            if success:
                return None, None, success, backtrackCount
            else:
                return None, [], success, backtrackCount

        startLoc = pattern.get_startLoc()
        start_x = startLoc[0]
        start_y = startLoc[1]
        direction = pattern.get_direction()
        length = pattern.get_length()

        #build Regex
        instantiated_lst = []
        ratio = get_ratio(start_x, start_y, direction, length, instantiated_lst, tileDict)
        if ratio == 1 and not pattern.is_instantiated():
            regex = build_regex(instantiated_lst)

            lst = query_wordpattern(pattern, regex)
            if lst:
                _, c = lst[0]
                pattern.set_clue(c)
                pattern.set_instantiated(True)

        if DEBUG:
            print("Ratio: " + str(ratio))

        # Keeps word pattern with the highest ratio (First encountered saved) that isn't fully instantiated
        if ratio > highest_ratio and ratio < 1:
            highest_ratio = ratio
            highest_ratio_letters = [instantiated_lst]
            highest_ratio_wp_lst = [pattern]
        elif ratio == highest_ratio:
            highest_ratio_letters.append(instantiated_lst)
            highest_ratio_wp_lst.append(pattern)

    if highest_ratio == -1:
        return None, highest_ratio_wp_lst, True, backtrackCount

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

    return most_constrained_wp,results, True, backtrackCount

def instantiate_wordpattern(pattern, results, tileDict, wordPatterns, intersectionDict, infoList, clues):
    if DEBUG:
        print("--------------------------------")
        print("INSTANTIATING WORD PATTERN:")
        print("PATTERN:")
        pattern.print_pattern()

        print("RESULTS: ")
        print(results)

        print("--------------------------------")
    #implement pick strategy

    # Create ClosedList object for
    closedList = QueryStructure(pattern, results)
    infoList.append(closedList)

    # Use the last word in the results list
    in_clues = True
    while in_clues:
        if not closedList.get_results():
            if DEBUG:
                print(clues)
                print("INSTANTIATE WORDPATTERN: all words used")
            return False
        (word, clue) = closedList.get_results()[-1]
        if (word, clue) not in clues:
            clues.append((word, clue))
            pattern.set_clue(clue)
            in_clues = False
        else:
            results.remove((word, clue))
            closedList.set_results(results)


    # Set tiles with given word
    startLoc = pattern.get_startLoc()
    start_x = startLoc[0]
    start_y = startLoc[1]
    direction = pattern.get_direction()
    patternLen = pattern.get_length()

    if direction == "across":
        if DEBUG:
            print(word)
        for i in range(patternLen):
            tile_loc = (start_x, start_y + i)
            tile = tileDict[tile_loc]
            if not tile.get_tile_state():
                if DEBUG:
                    print(word[i])
                tile.set_letter(word[i])
                tile.set_state(True)
                if tile.is_intersection():
                    wp_letters = []
                    intersect_wp = intersectionDict[tile_loc][1]
                    intersect_wp_loc= intersect_wp.get_startLoc()
                    intersect_dir = intersect_wp.get_direction()
                    intersect_len = intersect_wp.get_length()
                    ratio = get_ratio(intersect_wp_loc[0], intersect_wp_loc[1], intersect_dir, intersect_len, wp_letters, tileDict)
                    regex = build_regex(wp_letters)
                    freedom = get_freedom(intersect_wp, regex)
                    intersect_wp.set_freedom(freedom)
                    if ratio == 1 and not intersect_wp.is_instantiated():
                        lst = query_wordpattern(intersect_wp, regex)
                        if lst:
                            _, c = lst[0]
                            intersect_wp.set_clue(c)
                        intersect_wp.set_instantiated(True)


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
                    ratio = get_ratio(intersect_wp_loc[0], intersect_wp_loc[1], intersect_dir, intersect_len, wp_letters, tileDict)
                    regex = build_regex(wp_letters)
                    freedom = get_freedom(intersect_wp, regex)
                    intersect_wp.set_freedom(freedom)
                    if ratio == 1 and not intersect_wp.is_instantiated():
                        lst = query_wordpattern(intersect_wp, regex)
                        if lst:
                            _, c = lst[0]
                            intersect_wp.set_clue(c)
                        intersect_wp.set_instantiated(True)

    pattern.set_instantiated(True)
    return True

def find_Solution(tiling):
    '''
    <<<<<<<<<<<<<<<<<<Call BoardGenerator Functions: Generate Crossword Here>>>>>>>>>>>>>>>>>>>>
    '''
    # Analysis Dict
    backtrack_count = 0
    # list of all patterns being considered in queries and their results
    infoList = []

    # list containing (word, clue)
    clues = []

    '''
        Find all Word Patterns
    '''
    wordPatterns = BoardGenerator.get_wordPatterns(tiling)

    '''
        Set Freedoms of all word patterns
    '''
    set_freedom(wordPatterns)

    if DEBUG: 
        print("ALL Patterns ...")
        for wp in wordPatterns:
            wp.print_pattern()
            print("-----------------------------")

    '''
        Create Tile objects for each box
    '''
    d = len(tiling)

    if DEBUG:
        for i in range(d):
            for j in range(d):
                print("LOCATION: " + str(i) + ", " + str(j) + " ..... INTERSECTION: " + str(BoardGenerator.determine_intersection(i,j, wordPatterns)))

    tileDict, intersectionDict = BoardGenerator.get_Tiles(tiling, wordPatterns)

    if DEBUG:
        for tile in tileDict.values():
            tile.print_tileInfo()

    # print(tileDict)
    # print(intersectionDict)
    # print(len(wordPatterns))
    '''
        Get the seed for instantiation
    '''
    pattern, results = get_seed(wordPatterns, tileDict)
    seeded = instantiate_wordpattern(pattern, results, tileDict, wordPatterns, intersectionDict, infoList, clues)

    '''
        Get Board Soution
    '''
    if not seeded:
        print("FAILED TO SEED")

    valid_board = True
    while valid_board:
        if len(infoList) == len(wordPatterns):
            if DEBUG:
                print("COMPLETED BOARD")
            break
        
        wp, r, s, backtrack_count = choose_wordpattern(wordPatterns, tileDict, intersectionDict, infoList, clues, backtrack_count)

        while wp is None and r is None and s:
            wp, r, s, backtrack_count = choose_wordpattern(wordPatterns, tileDict, intersectionDict, infoList, clues, backtrack_count)
            if not infoList:
                print("INVALID BOARD PART i: NO MORE INFOLISTS")
                valid_board = False
                break

        if wp is None and len(r) == 0 and s:
            if DEBUG:
                print("COMPLETED SEARCH")
            break
        elif wp is None and len(r) == 0 and not s:
            print("INVALID BOARD PART ii: Ran out of words to use in backtracking")
            valid_board = False
            break
        else:
            success = instantiate_wordpattern(wp, r, tileDict, wordPatterns, intersectionDict, infoList, clues)
            success_backtrack = True
            if not success and len(infoList) > 0: 
                success_backtrack = backtrack(tileDict, intersectionDict, infoList, clues, backtrack_count)
            elif not success and not infoList:
                print("INVALID BOARD PART iii")
                valid_board = False
                break
            if not success_backtrack:
                print("INVALID BOARD PART iv")
                valid_board = False
                break

    return tileDict, wordPatterns, valid_board, backtrack_count