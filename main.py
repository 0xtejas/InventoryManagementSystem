import mysql.connector
from mysql.connector import errorcode
import json
import hashlib 
import getpass
from datetime import datetime
from os import system
from prettytable import PrettyTable 

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
    return rows



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
    cursor = con.cursor()
    stmt = "SELECT * FROM {table_name} WHERE {where}"  
    cursor.execute(stmt.format(table_name=table_name,where=where))
    rows = cursor.fetchall()
    return rows

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
        database=DB_NAME,
        buffered=True
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
        cols = extract_column_names(con,"users")
        index = 1
        for i in cols[1:-2]:
            print(f"{index}.Update {i}",end='\n')
            index += 1
        inp = input("Enter your choice: ")
        if inp == "1":
            roll_id_old = input("Enter OLD Roll ID: ")
            roll_id_new = input("Enter NEW Roll ID: ")
            update_data(con,"users",f"`roleId`='{roll_id_new}'",f"`roleId`='{roll_id_old}'")
            con.commit()
            con.close()
        elif inp == "2":
            first_name_old = input("Enter OLD First Name: ")
            first_name_new = input("Enter NEW First Name: ")
            update_data(con,"users",f"`firstName`='{first_name_new}'",f"`firstName`='{first_name_old}'")
            con.commit()
            con.close()
        elif inp == "3":
            middle_name_old = input("Enter OLD Middle Name: ")
            middle_name_new = input("Enter NEW Middle Name: ")
            update_data(con,"users",f"`middleName`='{middle_name_new}'",f"`middleName`='{middle_name_old}'")
            con.commit()
            con.close()
        elif inp == "4":
            last_name_old = input("Enter OLD Last Name: ")
            last_name_new = input("Enter NEW Last Name: ")
            update_data(con,"users",f"`lastName`='{last_name_new}'",f"`lastName`='{last_name_old}'")
            con.commit()
            con.close()
        elif inp == "5":
            username_old = input("Enter OLD Username: ")
            username_new = input("Enter NEW Username: ")
            update_data(con,"users",f"`username`='{username_new}'",f"`username`='{username_old}'")
            con.commit()
            con.close()
        elif inp == "6":
            mobile_old = input("Enter OLD Mobile: ")
            mobile_new = input("Enter NEW Mobile: ")
            update_data(con,"users",f"`mobile`='{mobile_new}'",f"`mobile`='{mobile_old}'")
            con.commit()
            con.close()
        elif inp == "7":
            email_old = input("Enter OLD Email: ")
            email_new = input("Enter NEW Email: ")
            update_data(con,"users",f"`email`='{email_new}'",f"`email`='{email_old}'")
            con.commit()
            con.close()
        elif inp == "8":
            password_old = getpass.getpass("Enter OLD Password: ")
            password_new = getpass.getpass("Enter NEW Password: ")
            password_new = hash_password(password_new)
            password_old = hash_password(password_old)
            update_data(con,"users",f"`passwordHash`='{password_new}'",f"`passwordHash`='{password_old}'")
            con.commit()
            con.close()


    elif inp == "3":
      display_data(con,"users")
      id = input("Enter ID of the user to be deleted: ")
      delete_data(con, "users",id)
    elif inp == "4":
        print("""
        1. Search by Roll ID
        2. Search by First Name
        3. Search by Middle Name
        4. Search by Last Name
        5. Search by Mobile
        6. Search by Email
        7. Search by Username
        8. Search by First Name
        9. Search by Registered Time
        10. Search by Last Login Time
        """)
        inp = input("Enter your choice: ")
        if inp == "1":
            roll_id = input("Enter Roll ID: ")
            values = search_data(con,"users","roleId = '{}'".format(roll_id))
        elif inp == "2":
            first_name = input("Enter First Name: ")
            values = search_data(con,"users","firstName = '{}'".format(first_name))
        elif inp == "3":
            middle_name = input("Enter Middle Name: ")
            values = search_data(con,"users","middleName = '{}'".format(middle_name))
        elif inp == "4":
            last_name = input("Enter Last Name: ")
            values = search_data(con,"users","lastName = '{}'".format(last_name))
        elif inp == "5":
            mobile = input("Enter Mobile Number: ")
            values = search_data(con,"users","mobile = '{}'".format(mobile))
        elif inp == "6":
            email = input("Enter Email ID: ")
            values = search_data(con,"users","email = '{}'".format(email))
        elif inp == "7":
            username = input("Enter Username Name: ")
            values = search_data(con,"users","username = '{}'".format(username))
        elif inp == "8":
            first_name = input("Enter First Name: ")
            values = search_data(con,"users","firstName = '{}'".format(first_name))
        elif inp == "9":
            registeredAt = input("Enter Registered Time: ")
            values = search_data(con,"users","registeredAt = '{}'".format(registeredAt))
        elif inp == "10":
            lastLoginAt = input("Enter Last Login Time: ")
            values = search_data(con,"users","lastLoginAt = '{}'".format(lastLoginAt))
        else:
            system("clear||cls")
            print("Invalid Choice")
            user_table()
        cols = extract_column_names(con,"users")
        cols.pop(8)
        myTable = PrettyTable(cols)
        values = display_data(con,"users")
        for i in values:
            myList = list(i)
            myList.pop(8)
            myTable.add_row(myList)
        print(myTable)

    elif inp == "5":
        cols = extract_column_names(con,"users")
        cols.pop(8)
        myTable = PrettyTable(cols)
        values = display_data(con,"users")
        for i in values:
            myList = list(i)
            myList.pop(8)
            myTable.add_row(myList)
        print(myTable)

    elif inp == "6":
      pass
    
def product_table(options):
    if options == "1":
        print(common_menu_banner.format("Product Table"))
    elif options == "2":
        print(common_menu_banner.format("Product Category Table"))
    elif options == "3":
        print(common_menu_banner.format("Product Meta Table"))
    
def order_table(options):
    if options == "1":
        print(common_menu_banner.format("Order"))
    elif options == "2":
        print(common_menu_banner.format("Order Item"))

def item_table(options):
    if options == "1":
        print(common_menu_banner.format("Item"))
        pass
    elif options == "2":
        print(common_menu_banner.format("Item Category"))
        pass
def transaction_table(options):
    pass

def category_table():
    pass

def address_table():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database=DB_NAME,
        buffered=True
      )
    print(common_menu_banner.format("Address"))
    inp = input("Enter your choice: ")
    if inp == "1":
        try:
            userID = input("Enter your user ID: ")
            orderID = input("Enter your order ID: ")
            firstName = input("Enter your first name: ")
            middleName = input("Enter your middle name: ")
            lastName = input("Enter your last name: ")
            mobile = input("Enter your mobile number: ")
            email = input("Enter Email ID: ")
            line1 = input("Enter your line 1: ")
            line2 = input("Enter your line 2: ")
            city = input("Enter your city: ")
            province = input("Enter your province: ")
            country = input("Enter your country: ")
            now = datetime.now()
            createdAt = now.strftime("%Y-%m-%d %H:%M:%S") 
            

            values = "(`userId`, `orderId`, `firstName`, `middleName`, `lastName`, `mobile`, `email`, `line1`, `line2`, `city`, `province`, `country`, `createdAt`) values({},{},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(userID,orderID,firstName,middleName,lastName,mobile,email,line1,line2,city,province,country,createdAt)

            insert_data(con,"address", values)

        except mysql.connector.IntegrityError:
            system("clear||cls")
            print("Check if you have filled values in Order table first!")
            order_table()
    elif inp == "2":
        cols = extract_column_names(con,"address")
        index = 1
        for i in cols[1:-1]:
            print(f"{index}.Update {i}",end='\n')
            index += 1
        inp = input("Enter your choice: ")
        if inp == "1":
            user_id_old = input("Enter OLD User ID: ")
            user_id_new = input("Enter NEW User ID: ")
            update_data(con,"address",f"`roleId`='{user_id_new}'",f"`roleId`='{user_id_old}'")
        elif inp == "2":
            order_id_old = input("Enter OLD Order ID: ")
            order_id_new = input("Enter NEW Order ID: ")
            update_data(con,"order",f"`orderId`='{order_id_new}'",f"`orderId`='{order_id_old}'")
        elif inp == "3":
            first_name_old = input("Enter OLD First Name: ")
            first_name_new = input("Enter NEW First Name: ")
            update_data(con,"address",f"`firstName`='{first_name_new}'",f"`firstName`='{first_name_old}'")
        elif inp == "4":
            middle_name_old = input("Enter OLD Middle Name: ")
            middle_name_new = input("Enter NEW Middle Name: ")
            update_data(con,"address",f"`middleName`='{middle_name_new}'",f"`middleName`='{middle_name_old}'")
        elif inp == "5":
            last_name_old = input("Enter OLD Last Name: ")
            last_name_new = input("Enter NEW Last Name: ")
            update_data(con,"address",f"`lastName`='{last_name_new}'",f"`lastName`='{last_name_old}'")
        elif inp == "6":
            mobile_old = input("Enter OLD Mobile: ")
            mobile_new = input("Enter NEW Mobile: ")
            update_data(con,"address",f"`mobile`='{mobile_new}'",f"`mobile`='{mobile_old}'")
        elif inp == "7":
            email_old = input("Enter OLD Email: ")
            email_new = input("Enter NEW Email: ")
            update_data(con,"address",f"`email`='{email_new}'",f"`email`='{email_old}'")
        elif inp == "8":
            line1_old = input("Enter OLD Line 1: ")
            line1_new = input("Enter NEW Line 1: ")
            update_data(con,"address",f"`line1`='{line1_new}'",f"`line1`='{line1_old}'")
        elif inp == "9":
            line2_old = input("Enter OLD Line 2: ")
            line2_new = input("Enter NEW Line 2: ")
            update_data(con,"address",f"`line2`='{line2_new}'",f"`line2`='{line2_old}'")
        elif inp == "10":
            city_old = input("Enter OLD City: ")
            city_new = input("Enter NEW City: ")
            update_data(con,"address",f"`city`='{city_new}'",f"`city`='{city_old}'")
        elif inp == "11":
            province_old = input("Enter OLD Province: ")
            province_new = input("Enter NEW Province: ")
            update_data(con,"address",f"`province`='{province_new}'",f"`province`='{province_old}'")
        elif inp == "12":
            country_old = input("Enter OLD Country: ")
            country_new = input("Enter NEW Country: ")
            update_data(con,"address",f"`country`='{country_new}'",f"`country`='{country_old}'")
        elif inp == "13":
            created_at_old = input("Enter OLD Created At: ")
            created_at_new = input("Enter NEW Created At: ")
            update_data(con,"address",f"`createdAt`='{created_at_new}'",f"`createdAt`='{created_at_old}'")

        now = datetime.now()
        updated_at_new =  now.strftime("%Y-%m-%d %H:%M:%S")
        update_data(con,"address",f"`updatedAt`='{updated_at_new}'",f"`updatedAt`= NULL")
        con.commit()
        con.close()
    elif inp == "3":
        display_data(con,"address")
        id = input("Enter ID of the address to be deleted: ")
        delete_data(con, "users",id)


def extract_column_names(con,table_name):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM {}".format(table_name))
    field_names = [i[0] for i in cursor.description]
    return field_names


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
