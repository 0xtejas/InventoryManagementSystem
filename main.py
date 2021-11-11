import mysql.connector
from mysql.connector import errorcode
import json
import hashlib.md5 as md5
import getpass

DB_NAME = "inventory"
with open("tables.json","r") as f:
    TABLES = json.load(f)

def menu():
    print("""
    1.  User Table
    2.  Product Table
    3.  Product Category Table
    4.  Product Meta Table
    5.  Order Table
    6.  Order Item Table
    7.  Item Table
    8.  Brand Table
    9.  Transaction Table
    10. Address Table
    11. Category Table
    12. Exit 
    """)
    inp = input("Enter your choice: ")
    return inp

################### PASSWORD HASHING FUNCTION ###################
def hash_password(password):
    return md5(password.encode()).hexdigest()


################### CREATE DATABASE #################

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


################### Initizalizing the Database and Table ###################

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

################### STANDARD QUERY STRUCTURE ###################

def insert_data(cursor,table_name,values):
  stmt = "INSERT INTO {table_name} {values}"
  cursor.execute(stmt.format(table_name=table_name,values=values))
  con.commit()
    
def display_data(cursor,table_name):
  stmt = "SELECT * FROM {table_name}"
  cursor.execute(stmt.format(table_name=table_name))
  rows = cursor.fetchall()
  for row in rows:
    print(row)



def update_data(cursor,table_name,values,where):
  stmt = "UPDATE {table_name} SET {values} WHERE {where}"
  cursor.execute(stmt.format(table_name=table_name,values=values,where=where))
  con.commit()

def delete_data(cursor,table_name,where):
  stmt = "DELETE FROM {table_name} WHERE {where}"
  cursor.execute(stmt.format(table_name=table_name,where=where))
  con.commit()
   

def search_data(cursor,table_name,where):
  stmt = "SELECT * FROM {table_name} WHERE {where}"  
  cursor.execute(stmt.format(table_name=table_name,where=where))
  rows = cursor.fetchall()
  for row in rows:
    print(row)


################### MAIN  ###################

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
      con.close()
      con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database=DB_NAME
      )
      choice = menu()
      
    
    else:
        print('Connection failed')
