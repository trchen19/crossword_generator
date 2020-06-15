import PySimpleGUI as sg
import random
import string
import UpdateBoard
import math

def draw_grid(tiling, box_size, clue_size, tile_dict, graph):
    for row in range(len(tiling)):
        for col in range(len(tiling[0])):
            currTile = None
            if tiling[row][col]:
                # Draw all white Tiles
                graph.draw_rectangle((col * box_size + 10, row * box_size + 10), (col * box_size + box_size + 10, row * box_size + box_size + 10), line_color='black')
                currTile = tile_dict[(row, col)]
                # Draw clue number if needed in a given tile
                # Draw Letters in tiles
                
                if currTile.get_tile_clue() != 0:
                    graph.draw_text( str(currTile.get_tile_clue()),
                                (col * box_size + 10 + (box_size//4), row * box_size + 10 +(box_size//4)), font=clue_size)
            else:
                # Blackout box if not valid tile
                graph.draw_rectangle((col * box_size + 10, row * box_size + 10), (col * box_size + box_size + 10, row * box_size + box_size + 10), line_color='black', fill_color='black')

def show_answers(tiling, dimension, text_size, box_size, clue_size, tile_dict, graph):
    for row in range(len(tiling)):
        for col in range(len(tiling[0])):
            currTile = None
            if tiling[row][col]:
                # Draw all white Tiles
                graph.draw_rectangle((col * box_size + 10 + dimension, row * box_size + 10), (col * box_size + box_size + 10 + dimension, row * box_size + box_size + 10), line_color='black')
                currTile = tile_dict[(row, col)]
                # Draw clue number if needed in a given tile
                # Draw Letters in tiles
                
                if currTile.get_tile_clue() != 0:
                    graph.draw_text( str(currTile.get_tile_clue()),
                                (col * box_size + 10 + (box_size//4)+ dimension, row * box_size + 10 +(box_size//4)), font=clue_size)
            else:
                # Blackout box if not valid tile
                graph.draw_rectangle((col * box_size + 10+ dimension, row * box_size + 10), (col * box_size + box_size + 10+ dimension, row * box_size + box_size + 10), line_color='black', fill_color='black')

    for loc, tile in tile_dict.items():
        graph.draw_text( str(tile.get_tile_letter()).lower(),
            (loc[1] * box_size + 10 + (box_size * .5) + dimension, loc[0] * box_size + 10 + (box_size * .5)), font=text_size)

def redraw_grid_and_letters(tiling, tile_dict, box_size, text_size, clue_size, graph):
    graph.erase()
    draw_grid(tiling, box_size, clue_size, tile_dict, graph)

    for loc, tile in tile_dict.items():
        if tile.get_user_letter() is not None:
            letter_location = (loc[1] * box_size + 10 + (box_size * .5), loc[0] * box_size + 10 +(box_size * .5))
            graph.draw_text('{}'.format(tile.get_user_letter().upper()),
                        letter_location, font=text_size)

def check_completion(tile_dict):
    for _, tile in tile_dict.items():
        if not tile.compare_answer():
            return False
    return True

def reset_grid(tiling, box_size, clue_size, tile_dict, graph):
    for _, tile in tile_dict.items():
        tile.set_user_letter(None)
    graph.erase()
    draw_grid(tiling, box_size, clue_size, tile_dict, graph)