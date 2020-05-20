import inputGenerator as inputGenerator
import BoardGenerator
import UpdateBoard
import math
from time import process_time
import os

querysize = 10

num_tilings = 100
ratio = 0.7
rows = 10
columns= 10

all_tilings = inputGenerator.get_tilings(num_tilings,rows,columns,ratio)
# all_tilings = [[[1,1,1,1,1,1,1,1,1,0,1,0],
#           [1,0,0,1,1,1,1,0,1,0,1,0],
#           [1,1,1,0,1,1,1,1,1,0,1,0],
#           [1,0,1,0,0,0,0,0,1,0,1,0],
#           [1,0,1,0,1,1,1,1,1,1,1,0],
#           [1,0,1,0,0,1,0,0,1,1,1,1],
#           [0,1,1,1,1,1,0,0,0,1,0,1],
#           [1,1,1,1,1,1,1,1,1,1,0,1],
#           [1,1,1,1,1,1,1,1,1,0,0,1],
#           [1,0,0,1,0,1,0,0,1,0,0,1]
#         ] ]

creation_success = []
succeded  = 0
failed = 0
true_ave_backtrack = 0
false_ave_backtrack = 0
true_ave_time = 0
false_ave_time = 0
ave_time = 0
ave_backtrack = 0
count = 1
for tiling in all_tilings:
    print("Executing Trial: " + str(count))
    start = process_time()
    tileDict, wordPatterns, valid_board, backtrack_count = UpdateBoard.find_Solution(tiling)
    end = process_time()
    time_elapsed = end - start
    creation_success.append((time_elapsed, valid_board, backtrack_count))

    ave_time += time_elapsed
    ave_backtrack += backtrack_count

    if valid_board:
            true_ave_time += time_elapsed
            true_ave_backtrack += backtrack_count
            succeded += 1
    else:
            false_ave_time += time_elapsed
            false_ave_backtrack += backtrack_count
            failed += 1
    count += 1

try:
    true_ave_backtrack = true_ave_backtrack/succeded
    true_ave_time = true_ave_time/succeded
except: 
    true_ave_backtrack = -1

try:
    false_ave_backtrack = false_ave_backtrack/failed
    false_ave_time = false_ave_time/failed

except: 
    false_ave_backtrack = -1

ave_time = ave_time/len(all_tilings)
ave_backtrack = ave_backtrack/len(all_tilings)

dirname = "limit_"+str(querysize)+"_ratio_" + str(ratio)
if not os.path.exists(dirname):
    os.makedirs(dirname)

filename = dirname + "/"+str(rows) + "x" + str(columns) +".txt"
f = open(filename, "w")
f.write("TRIALS: " + str(num_tilings) + ", Ratio: " + str(ratio) + ", Dimensions: " + str(rows) + "x" + str(columns))
f.write("\n")
f.write("\n")
for t, success, count in creation_success:
    f.write("Time Elapsed: " + str(t) + ", Success: " + str(success) + ", Backtracks: " + str(count))
    f.write("\n")
    f.write("------------------------------------------------")
    f.write("\n")

f.write("\n")
f.write("AVERAGE TIME: " + str(ave_time) + ", AVERAGE BACKTRACKS: " + str(ave_backtrack))
f.write("\n")
f.write("\n")

f.write("SUCCESSFUL BOARDS: " + str(succeded))
f.write("\n")
f.write("AVERAGE TIME (SUCCESS): " + str(true_ave_time) + ", AVERAGE BACKTRACKS: " + str(true_ave_backtrack))
f.write("\n")
f.write("\n")

f.write("FAILED BOARDS: " + str(failed))
f.write("\n")
f.write("AVERAGE TIME (SUCCESS): " + str(false_ave_time) + ", AVERAGE BACKTRACKS: " + str(false_ave_backtrack))
f.close()
