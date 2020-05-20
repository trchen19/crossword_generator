import PySimpleGUI as sg
import random
import string
import UpdateBoard
import math

DEBUG = False
PRINT_ANSWER = False
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
#           [1,1,1,1,1],
#           [1,1,1,1,1],
#           [1,1,1,1,1]
#         ]

# tiling = [[1,1,1,1],
#           [1,1,1,1],
#           [1,1,1,1],
#           [1,1,1,1]
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

# tiling = [[1,1,1,1,1,1,1,1,1,0,1,0],
#           [1,0,0,1,1,1,1,0,1,0,1,0],
#           [1,1,1,0,1,1,1,1,1,0,1,0],
#           [1,0,1,0,0,0,0,0,1,0,1,0],
#           [1,0,1,0,1,1,1,1,1,1,1,0],
#           [1,0,1,0,0,1,0,0,1,1,1,1],
#           [0,1,1,1,0,1,0,0,0,1,0,1],
#           [1,1,1,1,0,1,1,1,1,1,0,1],
#           [1,1,1,1,1,1,1,1,1,0,0,1],
#           [1,0,0,1,0,1,0,0,1,0,0,1],
#           [1,0,0,1,0,1,0,0,1,0,0,1],
#           [1,0,0,1,0,1,0,0,1,0,0,1]
#         ] 


tiling = [[1,1,1,1,1,1,1,1,1,0,1,0],
          [1,0,0,1,1,1,1,0,1,0,1,0],
          [1,1,1,0,1,1,1,1,1,0,1,0],
          [1,0,1,0,0,0,0,0,1,0,1,0],
          [1,0,1,0,1,1,1,1,1,1,1,0],
          [1,0,1,0,0,1,0,0,1,1,1,1],
          [0,1,1,1,1,1,0,0,0,1,0,1],
          [1,1,1,1,1,1,1,1,1,1,0,1],
          [1,1,1,1,1,1,1,1,1,0,0,1],
          [1,0,0,1,0,1,0,0,1,0,0,1]
        ] 

boardSize = len(tiling)
tileDict, wordPatterns, valid_board, backtrack_count = UpdateBoard.find_Solution(tiling)

# Tiles with letters filled in 
# Need: tileDict, tiling, wordPatterns, valid_board
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

if PRINT_ANSWER:
    for row in range(len(tiling)):
        for col in range(len(tiling[0])):
            currTile = None
            if tiling[row][col]:
                currTile = tileDict[(row, col)]
                if currTile.get_tile_letter() is not None:
                    g.draw_text( str(currTile.get_tile_letter()).lower(),
                                (col * BOX_SIZE + 18, row * BOX_SIZE +17), font='Courier 16')


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