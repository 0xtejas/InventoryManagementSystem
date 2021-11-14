import mysql.connector
from mysql.connector import errorcode
import json
import hashlib 
import getpass
from datetime import datetime
from os import system

DB_NAME = "inventory"
with open("tables.json","r") as f:
    TABLES = json.load(f)

################### STANDARD QUERY STRUCTURE ###################

def insert_data(con,table_name,values):
    cursor = con.cursor()
    stmt = "INSERT INTO {table_name} {values}"
    cursor.execute(stmt.format(table_name=table_name,values=values))
    con.commit()
    
def display_data(con,table_name):
    cursor = con.cursor()
    stmt = "SELECT * FROM {table_name}"
    cursor.execute(stmt.format(table_name=table_name))
    rows = cursor.fetchall()
    for row in rows:
      print(row)



def update_data(con,table_name,values,where):
    cursor = con.cursor()
    stmt = "UPDATE {table_name} SET {values} WHERE {where}"
    cursor.execute(stmt.format(table_name=table_name,values=values,where=where))
    con.commit()

def delete_data(con,table_name,where):
    cursor = con.cursor()
    stmt = "DELETE FROM {table_name} WHERE {where}"
    cursor.execute(stmt.format(table_name=table_name,where=where))
    con.commit()
   

def search_data(cursor,table_name,where):
  stmt = "SELECT * FROM {table_name} WHERE {where}"  
  cursor.execute(stmt.format(table_name=table_name,where=where))
  rows = cursor.fetchall()
  for row in rows:
    print(row)

####### MENU FUNCTIONS #######

common_menu_banner = """
    ##### {} MENU ##### 
    1. Insert 
    2. Update
    3. Delete
    4. Search
    5. Display
    6. Exit
"""

def user_table():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database=DB_NAME
      )
    print(common_menu_banner.format("User"))
    inp = input("Enter your choice: ")
    if inp == "1":
        try:
            roll_id = input("Enter Roll ID: ")
            first_name = input("Enter First Name: ")
            middle_name = input("Enter Middle Name: ")
            last_name = input("Enter Last Name: ")
            username = input("Enter Username Name: ")
            password = getpass.getpass("Enter Password: ")
            email = input("Enter Email ID: ")
            mobile = input("Enter Mobile Number: ")
            now = datetime.now()
            registeredAt =  now.strftime("%Y-%m-%d %H:%M:%S")

            password = hash_password(password)
            # insert into `users`  values('1','V','M','S','vm','9944145','bm@gmail.com','d73fbca9f19a294db16d18e225c61472','2021-11-14 21:32:17);
            values = "(`roleId`, `firstName`, `middleName`, `lastName`, `username`, `mobile`, `email`, `passwordHash`, `registeredAt`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(roll_id,first_name,middle_name,last_name,username,mobile,email,password,registeredAt)
            insert_data(con, "users", values)
            con.commit()
            con.close()
        except mysql.connector.IntegrityError:
            system("clear||cls")
            print("The Value Entered is DUPLICATE or Tampers the INTEGRITY of DataBase")
            user_table()

    elif inp == "2":
      pass
    elif inp == "3":
      pass
    elif inp == "4":
      pass
    elif inp == "5":
      pass
    elif inp == "6":
      pass
    
def product_table(options):
    if options == "1":
        # product table 
        pass
    elif options == "2":
        # product category table
        pass
    elif options == "3":
        # product meta table
        pass
    
def order_table(options):
    if options == "1":
        # order table 
        pass
    elif options == "2":
        # order item table
        pass

def item_table(options):
    if options == "1":
        # item table 
        pass
    elif options == "2":
        # brand table
        pass
def transaction_table(options):
    pass

def category_table():
    pass

def address_table(options):
    pass




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
    if inp == "1":
        user_table()
    elif inp == "2":
        product_table(1)
    elif inp == "3":
        product_table(2)
    elif inp == "4":
        product_table(3)
    elif inp == "5":
        order_table(1)
    elif inp == "6":
        order_table(2)
    elif inp == "7":
        item_table(1)
    elif inp == "8":
        item_table(2)
    elif inp == "9":
        transaction_table()
    elif inp == "10":
        address_table()
    elif inp == "11":
        category_table()
    elif inp == "12":
        exit(1)

################### PASSWORD HASHING FUNCTION ###################
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


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
