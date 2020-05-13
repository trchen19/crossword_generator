import PySimpleGUI as sg
import random
import string
import BoardGenerator
import UpdateBoard

DEBUG = False
BOX_SIZE = 25

layout = [
    [sg.Text('Crossword Puzzle Using PySimpleGUI'), sg.Text('', key='-OUTPUT-')],
    [sg.Graph((500, 500), (0, 450), (450, 0), key='graph',
              change_submits=True, drag_submits=False)],
    [sg.Button('Show'), sg.Button('Exit')]
]

window = sg.Window('Window Title', layout, finalize=True)

g = window['graph']

'''
<<<<<<<<<<<<<<<<<<Get user input here>>>>>>>>>>>>>>>>>>>>>
'''
# tiling = input("Please enter valid nxn 2D array: ")
## Insert input validation check here!! 
# tiling = [[1,1,1,1,1], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]
# tiling = [[1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0],[1,0,0,0,0]]
# tiling = [[1,1,1,1,1], [1,0,0,0,0], [1,0,0,0,0], [1,0,0,0,0],[1,0,0,0,0]]
# tiling = [[1,1,1,1,1], [0,0,1,0,0], [0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]]
# tiling = [[1,1,1,1,1], [0,0,1,0,0], [1,1,0,1,1],[0,0,1,0,0],[0,0,1,0,0]]
# tiling = [[1,1,1,1,1], [0,0,1,0,0], [1,1,0,1,1],[1,0,1,0,0],[1,0,1,0,0]] 
tiling = [[1,0,0,0,0,0,1,1,0,0],
          [1,0,0,1,0,0,1,0,0,0],
          [1,1,1,1,1,1,1,0,0,0],
          [1,0,0,1,0,0,0,0,0,0],
          [1,0,0,1,1,1,1,0,0,0],
          [1,0,0,0,0,1,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0],
          [0,0,0,1,1,1,1,1,0,0],
          [0,0,0,0,0,1,0,0,0,0],
        ] #Jo's tiling


'''
<<<<<<<<<<<<<<<<<<Call BoardGenerator Functions: Generate Crossword Here>>>>>>>>>>>>>>>>>>>>
'''
    
# list of all words being considered in queries
openList = []

# list containing (word, clue)
clue = []

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
    print(wordPatterns)
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

print(tileDict)
print(intersectionDict)
'''
    Get the seed for instantiation
'''
wp_idx = UpdateBoard.get_seed(wordPatterns, tileDict)

for row in range(len(tiling)):
    for col in range(len(tiling[0])):
        currTile = None
        if tiling[row][col]:
            # Draw all white Tiles
            g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black')
            currTile = tileDict[(row, col)]
            # Draw clue number if needed in a given tile
            if currTile.get_tile_clue() != 0:
                g.draw_text( str(currTile.get_tile_clue()),
                            (col * BOX_SIZE + 10, row * BOX_SIZE + 8))
        else:
            # Blackout box if not valid tile
            g.draw_rectangle((col * BOX_SIZE + 5, row * BOX_SIZE + 3), (col * BOX_SIZE + BOX_SIZE + 5, row * BOX_SIZE + BOX_SIZE + 3), line_color='black', fill_color='black')

# Start event loop
while True:             
    event, values = window.read()
    print(str(event) + " AND " + str(values))
    if event in (None, 'Exit'):
        break
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