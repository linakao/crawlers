import mysql.connector

password = '8888888'
DB_NAME = 'pchome'

cnx = mysql.connector.connect(user='root', password=password, host='127.0.0.1', database=DB_NAME)
cursor = cnx.cursor(dictionary=True)

query = ("SELECT * FROM products "
         "ORDER BY price")

cursor.execute(query)

for row in cursor:
  print(row)
  print(row['name'])

cursor.close()
cnx.close()