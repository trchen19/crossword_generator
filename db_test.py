import  mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1919myserver",
    database="mydatabase"
)

mycursor = mydb.cursor()      

sql = "SELECT * FROM words_4 WHERE term REGEXP 'a$' ORDER BY RAND() LIMIT 10"

mycursor.execute(sql)

results = mycursor.fetchall()
print(results)
