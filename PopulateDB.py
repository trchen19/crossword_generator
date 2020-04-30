# user: root
# pass: 1919myserver

import  mysql.connector
import csv

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1919myserver",
    database="mydatabase"
)

#extract word and only one respective clue from CSV

wordClues = {}
words = []

with open('American.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for word, clue in reader:
        temp = word.replace(" ", "")
        numLetters = len(temp)
        if str(numLetters) not in wordClues.keys():
            wordClues[str(numLetters)] = []
        if word not in words:
            words.append(word)
            wordClues[str(numLetters)].append((temp, clue))

# populate mydatabase with words and clues
mycursor = mydb.cursor()      
print(wordClues.keys())
print(wordClues["20"])
for numLetterStr in wordClues.keys():

    table_name = "words_" + numLetterStr


    mycursor.execute("CREATE TABLE "+table_name+" (term VARCHAR(255), clue VARCHAR(255))")
    print(table_name + " TABLE CREATED.....")
    print(mycursor.rowcount, "pre-insertion for table: "+ table_name)

    sql = "INSERT INTO " + table_name + " (term, clue) VALUES (%s, %s)"

    mycursor.executemany(sql, wordClues[numLetterStr])
    print(mycursor.rowcount, "Records inserted in table: "+ table_name)

    mydb.commit()
