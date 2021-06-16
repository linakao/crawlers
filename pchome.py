import requests
import time
import mysql.connector
from mysql.connector import errorcode

password = '8888888'
DB_NAME = 'pchome'


try:        
    cnx = mysql.connector.connect(user='root', password=password, host='127.0.0.1')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

cursor = cnx.cursor()

# Create database if not exist
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)


TABLES = {}
TABLES['products'] = (
    "CREATE TABLE `products` ("
    "  `no` int(5) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(60) NOT NULL,"
    "  `price` varchar(15) NOT NULL,"
    "  PRIMARY KEY (`no`)"
    ") ENGINE=InnoDB")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

add_products = ("INSERT INTO products "
               "(name, price) "
               "VALUES (%s, %s)")

# time interval
def sleep_time(hour, min, sec):
    return hour * 3600 + min * 60 + sec
 
second = sleep_time(0, 0, 5)

for i in range(1, 21):    
    url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%E6%B0%B4%E6%B3%A2%E7%88%90&page={}&sort=sale/dc'.format(i)
    r = requests.get(url)
    print('crawling page {}'.format(i))
    if r.status_code == requests.codes.ok:
        p = r.json()
        for i in p['prods']:
            name = i['name']
            price = int(i['price'])
            data_products = (name, price)
            cursor.execute(add_products, data_products)

    time.sleep(second)
    cnx.commit()

print('closing')
cursor.close()
cnx.close()