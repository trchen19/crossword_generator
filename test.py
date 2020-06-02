import re
s = "AVERAGE TIME: 0.00515625, AVERAGE BACKTRACKS: 0.02"

lst = re.split(r', | ', s)
print(lst)