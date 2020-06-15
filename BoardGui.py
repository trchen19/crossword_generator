import PySimpleGUI as sg
import random
import string
import UpdateBoard
import math
import gui_helper as gui_helper
import inputGenerator as inputGenerator
from threading import Timer
# import inputGenerator as inputGenerator

DEBUG = False
ANSWER_HIDDEN = True

sg.theme('Default1')
sg.theme_background_color('white')
sg.theme_element_background_color('white')

'''
<<<<<<<<<<<<<<<<<<Get user input here>>>>>>>>>>>>>>>>>>>>>
'''

# tiling = [ [1,1,1,0,1,1,1,1,0,1,1,1,1,1,1],
#            [0,1,0,0,1,0,1,0,0,1,0,0,1,0,1],
#            [0,1,0,0,1,0,1,0,0,1,0,0,1,1,1],
#            [1,1,1,1,1,0,1,1,1,1,1,0,1,0,1],
#            [1,0,0,1,0,0,1,0,0,1,0,0,1,0,0],
#            [1,1,1,1,1,1,1,0,0,1,0,1,1,1,1],
#            [1,0,0,1,0,0,1,1,1,1,0,0,1,0,1],
#            [1,0,1,1,1,1,1,0,1,0,0,0,1,1,1],
#            [0,0,0,1,0,0,0,0,1,0,1,0,0,0,1],
#            [1,0,1,0,0,0,0,0,1,0,1,0,1,0,1],
#            [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
#            [1,0,1,0,0,1,0,0,1,0,1,0,0,1,0],
#            [1,0,1,0,0,1,1,1,1,0,1,1,1,1,1],
#            [1,0,1,1,1,1,0,0,0,0,1,0,0,1,0],
#            [1,0,1,1,1,1,0,0,0,0,1,0,0,1,0]

# ]

# tiling = [ [1,1,1],
#             [0,0,0],
#             [0,0,0]
# ]
# tiling = inputGenerator.gen_valid_tiling(15,15,0.68)
while True:
    regenerate = False
    # Get User Parameters
    input_layout = [ 
        [sg.Text('Generated Crossword:', background_color='#FFFFFF', text_color='black'), sg.Text('', background_color='white', key='-OUTPUT-')],
        [sg.Text("Grid Dimension: ", background_color='#FFFFFF', text_color='black'), sg.Slider(range=(3,15),
            default_value=8,
            size=(18,15),
            orientation='horizontal',
            font=('Courier', 12))],
        [sg.Text("Diffculty: ", background_color='#FFFFFF', text_color='black'), sg.Combo(['Easy', 'Medium', 'Hard'])],
        [sg.Submit(), sg.Cancel()]
    ]

    input_window = sg.Window('Input Window', input_layout)    

    event, values = input_window.read()    
    input_window.close()
    d = int(values[0])
    diff = values[1]

    if diff == "Hard":
        ratio = 0.75
    elif diff == "Medium":
        ratio = 0.68
    else:
        ratio = 0.6

    tiling = inputGenerator.gen_valid_tiling(d, d, ratio)

    if tiling is None: 
        valid_board = False
    else:
        boardSize = len(tiling)
        BOX_SIZE = 330//boardSize

        dimension = BOX_SIZE * boardSize + 20
        bounds = (10, dimension-10)
        text_size = "Courier " + str(BOX_SIZE//2)
        clue_size = "Courier " + str(BOX_SIZE//3)
        tileDict, wordPatterns, valid_board, backtrack_count = UpdateBoard.find_Solution(tiling)

    '''
        Draw the Board With Relevant Metadata 
    '''

    col1 = []
    col2 = []

    if valid_board:
        across_lst = []
        down_lst = []
        for pattern in wordPatterns:
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

        count = 0
        while count < len(across_lst) or count < len(down_lst):
            try: 
                across = across_lst[count][1]
            except:
                across = None
            
            try:
                down = down_lst[count][1]
            except:
                down = None

            across_row = []
            if across is not None:
                across_row.append(sg.Text(across, auto_size_text=True, background_color='white'))
            else: 
                across_row.append(sg.Text('', background_color='white'))

            down_row = []
            if down is not None:
                down_row.append(sg.Text(down,  auto_size_text=True, background_color='white'))
            else: 
                down_row.append(sg.Text('', background_color='white'))
            
            col1.append(across_row)
            col2.append(down_row)
            count += 1

        crossword_layout = [
            [sg.Text('Generated Crossword:', background_color='#FFFFFF', text_color='black'), sg.Text('', background_color='white', key='-OUTPUT-')],
            [sg.Graph((dimension * 2, dimension), (0, dimension), (dimension*2, 0), key='graph', change_submits=True, drag_submits=False)],
            [sg.Text('CLUES: ', background_color='white', font='bold')],
            [sg.Text('ACROSS:', size=(40,1), background_color='white'), sg.Text('DOWN:', size=(40,1), background_color='white')],
            [sg.Column(col1, size=(300, dimension/2), scrollable=True), sg.Column(col2, size=(300, dimension/2), scrollable=True) ],
            [sg.Button('Check Answer'), sg.Button('Show Answer'), sg.Button('Hide Answer')], 
            [sg.Button("Generate New Board"), sg.Button('Reset Grid'), sg.Button('Exit')]
        ]
    else:
        crossword_layout = [
            [sg.Text('Generated Crossword:', background_color='#FFFFFF', text_color='black'), sg.Text('', background_color='white', key='-OUTPUT-')],
            [sg.Graph((dimension, dimension), (0, dimension), (dimension, 0), key='graph', change_submits=True, drag_submits=False)],
            [sg.Text('INVALID BOARD', background_color='#FFFFFF')],
            [sg.Button("Generate New Board"), sg.Button('Exit')]
        ]


    crossword_window = sg.Window('Automated Crossword', crossword_layout, finalize=True)
    crossword_window.maximize()
    g = crossword_window['graph']

    # Need: tileDict, tiling
    gui_helper.draw_grid(tiling, BOX_SIZE, clue_size, tileDict, g)

    # Start event loop
    while True:
        if gui_helper.check_completion(tileDict):
            g.draw_text("COMPLETED", (dimension//2, dimension//2), font="Courier 45 bold", color='red')             
        if not ANSWER_HIDDEN:
            gui_helper.show_answers(tiling, dimension, text_size, BOX_SIZE, clue_size, tileDict, g)

        event, values = crossword_window.read()
        
        if event in (None, 'Exit'):
            break
        
        if event in (None, 'Generate New Board'):
            regenerate = True
            break

        if event in (None, 'Reset Grid'):
            g.erase()
            gui_helper.reset_grid(tiling, BOX_SIZE, clue_size, tileDict, g)

        if event in (None, 'Show Answer'):
            ANSWER_HIDDEN = False

        if event in (None, 'Hide Answer'):
            gui_helper.redraw_grid_and_letters(tiling, tileDict, BOX_SIZE, text_size, clue_size, g)
            ANSWER_HIDDEN = True
                            
        if event in (None, 'Check Answer'):
            correct = True
            for loc, tile in tileDict.items():
                if tile.get_user_letter() is not None: 
                    print("loc: " + str(tile.get_tile_location()))

                    print("user: " + tile.get_user_letter())
                    print("answer: " + tile.get_tile_letter())

                    if not tile.compare_answer():
                        correct = False
                        g.draw_rectangle((loc[1] * BOX_SIZE + 10, loc[0] * BOX_SIZE + 10), 
                            (loc[1] * BOX_SIZE + BOX_SIZE + 10, loc[0] * BOX_SIZE + BOX_SIZE + 10), 
                                line_color='black', fill_color='red')
                        g.draw_text('{}'.format(tile.get_user_letter().upper()),
                                (loc[1] * BOX_SIZE + 10 + (BOX_SIZE * .5), 
                                    loc[0] * BOX_SIZE + 10 +(BOX_SIZE * .5)), font=text_size)

                        if tile.get_tile_clue() != 0:
                            g.draw_text( str(tile.get_tile_clue()),
                                    (loc[1] * BOX_SIZE + 10 + (BOX_SIZE//4), loc[0] * BOX_SIZE + 10 +(BOX_SIZE//4)), font=clue_size)
        
            t = Timer(30.0, gui_helper.redraw_grid_and_letters, [tiling, tileDict, BOX_SIZE, text_size, clue_size, g])
            t.start()

        mouse = values['graph']
        
        if event == 'graph':
            if mouse == (None, None):
                continue 

            in_x = mouse[0] >= bounds[0] and mouse[0] <= bounds[1]
            in_y = mouse[1] >= bounds[0] and mouse[1] <= bounds[1]
            if in_x and in_y:
                box_y = (mouse[0]-10)//BOX_SIZE
                box_x = (mouse[1]-10)//BOX_SIZE

                if (box_x, box_y) not in tileDict.keys():
                    continue 

                tile = tileDict[(box_x, box_y)]
                letter_location = (box_y * BOX_SIZE + 10 + (BOX_SIZE * .5), box_x * BOX_SIZE + 10 +(BOX_SIZE * .5))

                letter = sg.popup_get_text("Enter a Letter")
                if letter is None:
                    continue
                elif letter == '':
                    tile.set_user_letter(None)
                    gui_helper.redraw_grid_and_letters(tiling, tileDict, BOX_SIZE, text_size, clue_size, g)
                    continue

                while True:
                    if letter == '':
                        tile.set_user_letter(None)
                        gui_helper.redraw_grid_and_letters(tiling, tileDict, BOX_SIZE, text_size, clue_size, g)
                        continue
                    if len(letter) > 1 or not letter.isalpha():
                        letter = sg.popup_get_text("Invalid entry. Enter a Letter")
                        if letter is None:
                            continue
                    else:
                        break


                if tile.get_user_letter() is not None:
                    tile.set_user_letter(letter.lower())
                    gui_helper.redraw_grid_and_letters(tiling, tileDict, BOX_SIZE, text_size, clue_size, g)
                else:
                    tile.set_user_letter(letter.lower())
                    g.draw_text('{}'.format(letter.upper()),
                                letter_location, font=text_size)
            else:
                continue

    crossword_window.close()

    if not regenerate:
        break