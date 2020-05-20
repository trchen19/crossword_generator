import random as random
import math
import numpy as np

def gen_tiling(num_rows, num_cols, ratio):
    tiling = np.zeros((num_rows, num_cols), dtype=int)
        
    total_squares = num_cols * num_rows
    num_tiles = round(ratio * total_squares)
    tiles_created = 0    
    while tiles_created < num_tiles:
        x = random.randint(0, num_rows-1)
        y = random.randint(0, num_cols-1)
        if not tiling[x, y]:
            tiling[x,y] = 1
            tiles_created += 1
    return tiling, num_tiles

def verify_tiling(tiling, num_tiles):
    # rows, cols = np.shape(tiling)
    valid = set()
    rows = len(tiling)
    cols = len(tiling[0])
    # Look for across validity
    for i in range(rows):
        patternLen = 0
        for j in range(cols):
            if tiling[i][j]:
                patternLen += 1
                if j == cols-1 and patternLen >2:
                    for u in range(patternLen):  
                        valid.add((i,j-u))
            elif not tiling[i][j] and patternLen > 2:
                for u in range(patternLen):  
                    valid.add((i,j-(u+1)))
                patternLen = 0
                
            else:
                patternLen = 0

    # find patterns in every down (i.e. down word patterns)
    for j in range(cols):
        patternLen = 0
        for i in range(rows):
            if tiling[i][j]:
                patternLen += 1
                if i == rows-1 and patternLen >2:
                    for u in range(patternLen):  
                        valid.add((i-u,j))
            elif not tiling[i][j] and patternLen > 2:
                for u in range(patternLen):  
                    valid.add((i-(u+1),j))
                patternLen = 0
            else:
                patternLen = 0

    return len(valid) == num_tiles

def get_tilings(num_tilings, num_rows, num_cols, ratio):
    print("Getting Tilings...")
    all_tilings = []
    count = 0
    while len(all_tilings) < num_tilings:
        tiling, num_tiles = gen_tiling(num_rows, num_cols, ratio)
        b = verify_tiling(tiling, num_tiles)
        if b:
            in_lst = False
            for t in all_tilings:
                comparison = tiling == t
                if comparison.all():
                    in_lst = True
            if not in_lst:
                all_tilings.append(tiling)
        count+=1
            
        if count == 200000:
            break
    print("Finished Generating Tilings...")

    return all_tilings



