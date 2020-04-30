import mysql.connector
import Tile

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1919myserver",
    database="mydatabase"
)

mycursor = mydb.cursor()

def set_freedom(wordPatterns):
    for pattern in wordPatterns:
        patternLen = pattern[2]
        #setting initial freedome values for all wordpatterns
        # Query appropriate DB table given patternLen --> save rowcount as pattern freedom score (i.e pattern[3])
        sql = "SELECT COUNT(*) FROM words_"+str(patternLen)
        mycursor.execute(sql)
        (freedom,_) = mycursor.fetchone()
        pattern[3] = freedom
    
def get_seed(wordPatterns, tileDict):
    # Find word pattern with the most intersections 
    most_intersect = 0
    most_idx = -1
    count = 0

    for pattern in wordPatterns:
        numIntersection = 0
        patternLen = pattern[2]

        #count number of intersections 
        startLoc = pattern[0]
        x = startLoc[0]
        y = startLoc[1]

        if pattern[1] == "across":
            for i in range(patternLen):
                tile = tileDict[(x, y+i)]
                if tile.is_intersection():
                    numIntersection += 1
        else:
            for i in range(patternLen):
                tile = tileDict[(x+i, y)]
                if tile.is_intersection():
                    numIntersection += 1
        
        if numIntersection > most_intersect:
            most_intersect = numIntersection
            most_idx = count

        count += 1
        
    return most_idx

def choose_wordpattern(wordPatterns, tileDict):
    # Implement most_constrained
    pass

def instantiate_wordpattern(wordpattern):
    #implement pick strategy
    pass