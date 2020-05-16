import PySimpleGUI as sg
import random
import string
import BoardGenerator
import UpdateBoard
import math

DEBUG = False
PRINT_ANSWER = True
BOX_SIZE = 23

layout = [
    [sg.Text('Crossword Puzzle Using PySimpleGUI'), sg.Text('', key='-OUTPUT-')],
    [sg.Graph((600, 600), (0, 550), (550, 0), key='graph',
              change_submits=True, drag_submits=False)],
    [sg.Button('Show Answer'), sg.Button('Exit')]
]

window = sg.Window('Window Title', layout, finalize=True)

g = window['graph']

'''
<<<<<<<<<<<<<<<<<<Get user input here>>>>>>>>>>>>>>>>>>>>>
'''
# tiling = input("Please enter valid nxn 2D array: ")
# Insert input validation check here!! 
# tiling = [[1,1,1,1,1], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]
# tiling = [[1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0],[1,0,0,0,0]]
# tiling = [[1,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0],[1,0,0,0,0]]
# tiling = [[1,1,1,1,1], [0,0,1,0,0], [0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]]
# tiling = [[1,1,1,1,1], [0,0,1,0,0], [1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0]]
# tiling = [[1,1,1,1,1], [0,0,1,0,0], [1,1,0,1,1],[1,0,1,0,0],[1,0,1,0,0]] 
# tiling = [[1,1,1,1,1], [0,0,1,0,0], [1,1,1,1,1],[1,0,1,0,0],[1,0,1,0,0]] 

# tiling = [[1,0,0,0,0,0,1,1,1,0],
#           [1,0,0,1,0,0,1,0,0,0],
#           [1,1,1,1,1,1,1,0,0,0],
#           [1,0,0,1,0,0,0,0,0,0],
#           [1,0,0,1,1,1,1,0,0,0],
#           [1,0,0,0,0,1,0,0,0,0],
#           [0,0,0,0,0,1,0,0,0,0],
#           [0,0,0,0,0,1,0,0,0,0],
#           [0,0,0,1,1,1,1,1,0,0],
#           [0,0,0,0,0,1,0,0,0,0]
#         ] #Jo's tiling

# tiling = [[1,1,1,1,1],
#           [1,1,1,1,1],
#           [1,0,1,1,1],
#           [1,1,1,1,1],
#           [1,1,1,1,1]
#         ]

# tiling = [[1,1,1,1,1],
#           [1,1,1,1,1],
#           [1,0,1,0,1],
#           [1,1,1,1,1],
#           [1,1,1,1,1]
#         ]

# tiling = [[1,0,0,1,1,1,1,1,1,0],
#           [1,0,0,1,1,1,1,0,1,0],
#           [1,1,1,0,1,1,1,1,1,0],
#           [1,0,0,0,0,0,0,0,1,0],
#           [1,0,0,0,1,1,1,1,1,1],
#           [1,0,0,0,0,1,0,0,1,1],
#           [0,1,0,1,0,1,0,0,0,1],
#           [1,1,1,1,0,1,1,1,1,1],
#           [1,1,0,1,1,1,1,1,1,0],
#           [1,0,0,1,0,1,0,0,1,0]
#         ] 

# tiling = [[1,1,1,1,1,1,1,1,1,0],
#           [1,0,0,1,1,1,1,0,1,0],
#           [1,1,1,0,1,1,1,1,1,0],
#           [1,0,1,0,0,0,0,0,1,0],
#           [1,0,1,0,1,1,1,1,1,1],
#           [1,0,1,0,0,1,0,0,1,1],
#           [0,1,1,1,0,1,0,0,0,1],
#           [1,1,1,1,0,1,1,1,1,1],
#           [1,1,1,1,1,1,1,1,1,0],
#           [1,0,0,1,0,1,0,0,1,0]
#         ] 

tiling = [[1,1,1,1,1,1,1,1,1,0,1,0],
          [1,0,0,1,1,1,1,0,1,0,1,0],
          [1,1,1,0,1,1,1,1,1,0,1,0],
          [1,0,1,0,0,0,0,0,1,0,1,0],
          [1,0,1,0,1,1,1,1,1,1,1,0],
          [1,0,1,0,0,1,0,0,1,1,1,1],
          [0,1,1,1,0,1,0,0,0,1,0,1],
          [1,1,1,1,0,1,1,1,1,1,0,1],
          [1,1,1,1,1,1,1,1,1,0,0,1],
          [1,0,0,1,0,1,0,0,1,0,0,1],
          [1,0,0,1,0,1,0,0,1,0,0,1],
          [1,0,0,1,0,1,0,0,1,0,0,1]
        ] 


# tiling = [[1,1,1,1,1,1,1,1,1,0,1,0],
#           [1,0,0,1,1,1,1,0,1,0,1,0],
#           [1,1,1,0,1,1,1,1,1,0,1,0],
#           [1,0,1,0,0,0,0,0,1,0,1,0],
#           [1,0,1,0,1,1,1,1,1,1,1,0],
#           [1,0,1,0,0,1,0,0,1,1,1,1],
#           [0,1,1,1,1,1,0,0,0,1,0,1],
#           [1,1,1,1,1,1,1,1,1,1,0,1],
#           [1,1,1,1,1,1,1,1,1,0,0,1],
#           [1,0,0,1,0,1,0,0,1,0,0,1]
#         ] 

boardSize = len(tiling)
'''
<<<<<<<<<<<<<<<<<<Call BoardGenerator Functions: Generate Crossword Here>>>>>>>>>>>>>>>>>>>>
'''
    
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
UpdateBoard.set_freedom(wordPatterns)

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
print(len(wordPatterns))
'''
    Get the seed for instantiation
'''
pattern, results = UpdateBoard.get_seed(wordPatterns, tileDict)
seeded = UpdateBoard.instantiate_wordpattern(pattern, results, tileDict, wordPatterns, intersectionDict, infoList, clues)

'''
    Get Board Soution
'''
if not seeded:
    print("FAILED TO SEED")

valid_board = True
while valid_board:
    if len(infoList) == len(wordPatterns):
        print("COMPLETED BOARD")
        break
    
    wp, r, s = UpdateBoard.choose_wordpattern(wordPatterns, tileDict, intersectionDict, infoList, clues)

    while wp is None and r is None and s:
        wp, r, s = UpdateBoard.choose_wordpattern(wordPatterns, tileDict, intersectionDict, infoList, clues)
        if not infoList:
            print("INVALID BOARD PART i: NO MORE INFOLISTS")
            valid_board = False
            break

    if wp is None and len(r) == 0 and s:
        #NOT VALID: CASE WHEN FREEDOM AND EVERYTHING > 0 BUT QUERY RESULTS RETURN [].... OUTPUT FROM CHOOSE WORDPATTERN IS (PATTERN, [])
        #NEED TO CHANGE PREVIOUS WORDS AND POTENTIALLY BACKTRACK 
        print("Completed Search")
        break
    elif wp is None and len(r) == 0 and not s:
        print("INVALID BOARD PART ii")
        valid_board = False
        break
    else:
        success = UpdateBoard.instantiate_wordpattern(wp, r, tileDict, wordPatterns, intersectionDict, infoList, clues)
        success_backtrack = True
        if not success and len(infoList) > 0: 
            success_backtrack = UpdateBoard.backtrack(tileDict, intersectionDict, infoList, clues)
        elif not success and not infoList:
            print("INVALID BOARD PART iii")
            valid_board = False
            break
        if not success_backtrack:
            print("INVALID BOARD PART iv")
            valid_board = False
            break
# Tiles with letters filled in 

# ****************Still need to associate clues with appropriate words/Tiles****************

for row in range(len(tiling)):
    for col in range(len(tiling[0])):
        currTile = None
        if tiling[row][col]:
            # Draw all white Tiles
            g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')
            currTile = tileDict[(row, col)]
            # Draw clue number if needed in a given tile
            # Draw Letters in tiles
            
            if currTile.get_tile_clue() != 0:
                g.draw_text( str(currTile.get_tile_clue()),
                            (col * BOX_SIZE + 12, row * BOX_SIZE + 10))
        else:
            # Blackout box if not valid tile
            g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color='black')


if valid_board:
    g.draw_text("CLUES:", (267.5, boardSize * BOX_SIZE + 25), font='Courier 18', text_location="center")
    g.draw_text("ACROSS:", (125, boardSize * BOX_SIZE + 50), font='Courier 16', text_location="center")
    g.draw_text("DOWN:", (400, boardSize * BOX_SIZE + 50), font='Courier 16', text_location="center")
    across_lst = []
    down_lst = []
    for pattern in wordPatterns:
        if DEBUG:
            print("CLUE NUM: ")
            print(pattern.get_clueNum())
            print("CLUE: ")
            print(pattern.get_clue())
        try:
            s = str(pattern.get_clueNum()) + ". " + pattern.get_clue() 
        except:
            s = str(pattern.get_clueNum()) + ". INVALID BOARD"
        if pattern.get_direction() == "across": 
            across_lst.append((pattern.get_clueNum(), s))
        if pattern.get_direction() == "down": 
            down_lst.append((pattern.get_clueNum(), s))

    across_lst = sorted(across_lst, key=lambda x: x[0])
    down_lst = sorted(down_lst, key=lambda x: x[0])

    for i in range(len(across_lst)):
        g.draw_text( across_lst[i][1], (125, i * 15 + (boardSize * BOX_SIZE + 75)), font='Courier 8', text_location="center")
    for i in range(len(down_lst)):
        g.draw_text( down_lst[i][1], (400, i * 15 +(boardSize * BOX_SIZE + 75)), font='Courier 8')
else:
    g.draw_text("BOO! INVALID BOARD", (267.5, boardSize * BOX_SIZE + 25), font='Courier 18', text_location="center")



# Start event loop
while True:             
    event, values = window.read()
    print(str(event) + " AND " + str(values))
    if event in (None, 'Exit'):
        break

    if event in (None, 'Show Answer'):
        for row in range(len(tiling)):
            for col in range(len(tiling[0])):
                currTile = None
                if tiling[row][col]:
                    currTile = tileDict[(row, col)]
                    if currTile.get_tile_letter() is not None:
                        g.draw_text( str(currTile.get_tile_letter()).lower(),
                                    (col * BOX_SIZE + 18, row * BOX_SIZE +17), font='Courier 18')

    mouse = values['graph']
    print(mouse)
    
    if event == 'graph':
        if mouse == (None, None):
            continue
        box_x = mouse[0]//BOX_SIZE
        box_y = mouse[1]//BOX_SIZE
        letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
        print(box_x, box_y)
        
        # Once box is clicked, prompt user letter input 
        # Then draw desired letter in box 
        # CHOICE: CHECK IF CORRECT LETTER --> DENY IF IN CORRECT or JUST LET IT HAPPEN.... HAVE A SHOW ANSWER OPTION 
        g.draw_text('{}'.format(random.choice(string.ascii_uppercase)),
                    letter_location, font='Courier 25')

window.close()