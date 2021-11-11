import mysql.connector
from mysql.connector import errorcode
import json

DB_NAME = "inventory"
with open("tables.json","r") as f:
    TABLES = json.load(f)

def create_database(cursor):
    
    try:
        cursor.execute(
            "CREATE  DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except:
        print("Database {}: already exist.".format(DB_NAME))


    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            con.database = DB_NAME
        else:
            print(err)
            exit(1)



def initialize(con): 
    cursor = con.cursor()
    create_database(cursor)

    

# TABLE CREATION    
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
    print(f"Total Number of Table Queries: {len(TABLES)}")
    cursor.close()
    con.close()

if __name__ == '__main__':
    # TEST MYSQL CONNECTIONS
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
    )
    if con.is_connected():
        print('Connected to MySQL database')
        initialize(con)
    else:
        print('Connection failed')
