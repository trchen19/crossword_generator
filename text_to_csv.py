import csv 
import os
import re 

querysize = 300

ratio = 0.85
# i = 4

rows = []
dirname = "limit_"+str(querysize)+"_ratio_" + str(ratio)
if not os.path.exists(dirname):
    print("CAN'T FIND DIR")

for i in range(4,10):
    filename = dirname + "/"+str(i) + "x" + str(i) +".txt"
    with open(filename) as f:
            lst = []
            for j, line in enumerate(f):
                if j == 203:
                    temp = re.split(r', | ', line)
                    lst.append(temp[2])
                    lst.append(temp[5])
                    #     AVERAGE TIME: 0.0026041666666666665, AVERAGE BACKTRACKS: 0.0
                elif j == 205: 
                    temp = re.split(r', | ', line)
                    lst.append(temp[2])

                #     SUCCESSFUL BOARDS: 6
                elif j == 206:
                    temp = re.split(r', | ', line)
                    lst.append(temp[3])
                    lst.append(temp[6])
                        
                #     AVERAGE TIME (SUCCESS): 0.0026041666666666665, AVERAGE BACKTRACKS: 0.0
                elif j == 208:
                    temp = re.split(r', | ', line)
                    lst.append(temp[2])
                    #     FAILED BOARDS: 0
                elif j == 209:
                    temp = re.split(r', | ', line)
                    lst.append(temp[3])
                    lst.append(temp[6])
            rows.append(lst)

# filename = dirname + "/"+str(i) + "x" + str(i) +".txt"
# with open(filename) as f:
#         lst = []
#         for j, line in enumerate(f):
#             if j == 203:
#                 temp = re.split(r', | ', line)
#                 lst.append(temp[2])
#                 lst.append(temp[5])
#                 #     AVERAGE TIME: 0.0026041666666666665, AVERAGE BACKTRACKS: 0.0
#             elif j == 205: 
#                 temp = re.split(r', | ', line)
#                 lst.append(temp[2])

#             #     SUCCESSFUL BOARDS: 6
#             elif j == 206:
#                 temp = re.split(r', | ', line)
#                 lst.append(temp[3])
#                 lst.append(temp[6])
                    
#             #     AVERAGE TIME (SUCCESS): 0.0026041666666666665, AVERAGE BACKTRACKS: 0.0
#             elif j == 208:
#                 temp = re.split(r', | ', line)
#                 lst.append(temp[2])
#                 #     FAILED BOARDS: 0
#             elif j == 209:
#                 temp = re.split(r', | ', line)
#                 lst.append(temp[3])
#                 lst.append(temp[6])
#         rows.append(lst)
            #     AVERAGE TIME (SUCCESS): 0, AVERAGE BACKTRACKS: -1

with open('results.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerows(rows)
