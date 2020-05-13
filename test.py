from Tile import InfoStructure, Tile, WordPattern

wordPatterns = []

for i in range(10):
    loc = (i,i)
    wordPatterns.append(WordPattern(loc, "across", 10, 0))

for pattern in wordPatterns:
    pattern.set_direction("down")
    pattern.print_pattern()
