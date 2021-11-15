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
    print(cursor.statement)
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
            values = "(`roleId`, `firstName`, `middleName`, `lastName`, `username`, `mobile`, `email`, `passwordHash`, `registeredAt`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(roll_id,first_name,middle_name,last_name,username,mobile,email,password,registeredAt)
            insert_data(con, "users", values)
            con.commit()
            con.close()
        except mysql.connector.IntegrityError:
            con.rollback()
            system("clear||cls")
            print("The Value Entered is DUPLICATE or Tampers the INTEGRITY of DataBase")
            user_table()

            con.rollback()
    elif inp == "2":
        cols = extract_column_names(con,"users")
        cols.pop(8)
        myTable = PrettyTable(cols)
        values = display_data(con,"users")
        for i in values:
            myList = list(i)
            myList.pop(8)
            myTable.add_row(myList)
        print(myTable)

        index = 1
        for i in cols[1:-2]:
            print(f"{index}.Update {i}",end='\n')
            index += 1
        inp = input("Enter your choice: ")
        id = input("Enter ID: ")
        if  inp == "1":
            id_new = int(input("Enter NEW ID: "))
            update_data(con,"users",f"`roleId` = '{id_new}'",f"`id` = '{id}'")
        elif inp == "2":
            first_name = input("Enter NEW First Name: ")
            update_data(con,"users",f"`firstName` = '{first_name}'",f"`id` = '{id}'")
        elif inp == "3":
            middle_name = input("Enter NEW Middle Name: ")
            update_data(con,"users",f"`middleName` = '{middle_name}'",f"`id` = '{id}'")
        elif inp == "4":
            last_name = input("Enter NEW Last Name: ")
            update_data(con,"users",f"`lastName` = '{last_name}'",f"`id` = '{id}'")
        elif inp == "5":
            username = input("Enter NEW Username: ")
            update_data(con,"users",f"`username` = '{username}'",f"`id` = '{id}'")
        elif inp == "6":
            mobile = input("Enter NEW Mobile: ")
            update_data(con,"users",f"`mobile` = '{mobile}'",f"`id` = '{id}'")
        elif inp == "7":
            email = input("Enter NEW Email: ")
            update_data(con,"users",f"`email` = '{email}'",f"`id` = '{id}'")
        else:
            system("clear||cls")
            print("Invalid Choice")
            user_table()
        
    elif inp == "3":
        cols = extract_column_names(con,"users")
        cols.pop(8)
        myTable = PrettyTable(cols)
        values = display_data(con,"users")
        for i in values:
            myList = list(i)
            myList.pop(8)
            myTable.add_row(myList)
        print(myTable)

        id = input("Enter ID of the user to be deleted: ")
        delete_data(con, "users",id)
    elif inp == "4":
        cols = extract_column_names(con,"users")
        index = 1
        cols.pop(8)
        for i in cols[1:]:
            print(f"{index}. Select by {i}",end='\n')
            index += 1
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
def transaction_table():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database=DB_NAME,
        buffered=True
      )
    print(common_menu_banner.format("Transaction"))
    inp = input("Enter your choice: ")
    if inp == "1":
        try:
            userId = input("Enter your user ID: ")
            orderId = input("Enter your order ID: ")
            code = input("Enter your code: ")
            type = input("Enter your type: ")
            mode = input("Enter your mode: ")
            amount = input("Enter your amount: ")
            status = input("Enter your status: ")
            now = datetime.now()   
            createdAt = now.strftime("%Y-%m-%d %H:%M:%S")

            values = "(`userId`, `orderId`, `code`, `type`, `mode`, `status`, `createdAt`) values('{}','{}','{}','{}','{}','{}','2021-11-15 20:29:12')".format(userId,orderId,code,type,mode,status,createdAt)
            insert_data(con,"transaction",values)
        except mysql.connector.Error:
            con.rollback()
            system("clear||cls")
            print("The Value Entered is DUPLICATE or Tampers the INTEGRITY of DataBase")
            transaction_table()
    elif inp == "2":
        cols = extract_column_names(con,"transaction")
        myTable = PrettyTable(cols)
        values = display_data(con,"transaction")

        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)
        
        index = 1
        for i in cols[1:-1]:
            print(f"{index}. Update {i}",end='\n')
            index += 1
        inp = input("Enter your choice: ")    
        id = input("Enter the ID: ")

        if inp == "1":
            userId_new = input("Enter your user ID: ")
            update_data(con,"transaction",f"`userId` = '{userId_new}'",f"`id` = '{id}'")
        elif inp == "2":
            orderId_new = input("Enter your order ID: ")
            update_data(con,"transaction",f"`orderId` = '{orderId_new}'",f"`id` = '{id}'")
        elif inp == "3":
            code_new = input("Enter your code: ")
            update_data(con,"transaction",f"`code` = '{code_new}'",f"`id` = '{id}'")
        elif inp == "4":
            type_new = input("Enter your type: ")
            update_data(con,"transaction",f"`type` = '{type_new}'",f"`id` = '{id}'")
        elif inp == "5":
            mode_new = input("Enter your mode: ")
            update_data(con,"transaction",f"`mode` = '{mode_new}'",f"`id` = '{id}'")
        elif inp == "6":
            amount_new = input("Enter your amount: ")
            update_data(con,"transaction",f"`amount` = '{amount_new}'",f"`id` = '{id}'")
        elif inp == "7":
            status_new = input("Enter your status: ")
            update_data(con,"transaction",f"`status` = '{status_new}'",f"`id` = '{id}'")
        elif inp == "8":
            createdAt_new = input("Enter your createdAt: ")
            update_data(con,"transaction",f"`createdAt` = '{createdAt_new}'",f"`id` = '{id}'")
        else:
            system("clear||cls")
            print("Invalid input!")
            transaction_table()
        
        now = datetime.now()
        updated_at_new =  now.strftime("%Y-%m-%d %H:%M:%S")
        update_data(con,"transaction",f"`updatedAt`='{updated_at_new}'",f"`id`= {id}")
        con.commit()
        con.close()


        pass
    elif inp == "3":
        cols = extract_column_names(con,"transaction")
        myTable = PrettyTable(cols)
        values = display_data(con,"transaction")
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)

        id = input("Enter ID of the user to be deleted: ")
        delete_data(con, "transaction", f"`id` = '{id}'")
    elif inp == "4":
        cols = extract_column_names(con,"transaction")
        index = 1
        cols.pop(8)
        for i in cols[1:]:
            print(f"{index}. Select by {i}",end='\n')
            index += 1
        inp = input("Enter your choice: ") 
        if inp == "1":
            userId = input("Enter your user ID: ")
            values = search_data(con,"transaction",f"`userId` = '{userId}'")
        elif inp == "2":
            orderId = input("Enter your order ID: ")
            values = search_data(con,"transaction",f"`orderId` = '{orderId}'")
        elif inp == "3":
            code = input("Enter your code: ")
            values = search_data(con,"transaction",f"`code` = '{code}'")
        elif inp == "4":
            type = input("Enter your type: ")
            values = search_data(con,"transaction",f"`type` = '{type}'")
        elif inp == "5":
            mode = input("Enter your mode: ")
            values = search_data(con,"transaction",f"`mode` = '{mode}'")
        elif inp == "6":
            amount = input("Enter your amount: ")
            values = search_data(con,"transaction",f"`amount` = '{amount}'")
        elif inp == "7":
            status = input("Enter your status: ")
            values = search_data(con,"transaction",f"`status` = '{status}'")
        elif inp == "8":
            createdAt = input("Enter your createdAt: ")
            values = search_data(con,"transaction",f"`createdAt` = '{createdAt}'")
        else:
            system("clear||cls")
            print("Invalid input!")
            transaction_table()

        cols = extract_column_names(con,"transaction")
        myTable = PrettyTable(cols)
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)
    elif inp == "5":
        cols = extract_column_names(con,"transaction")
        myTable = PrettyTable(cols)
        values = display_data(con,"transaction")
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)      


def category_table():
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database=DB_NAME,
        buffered=True
      )
    print(common_menu_banner.format("Category"))
    inp = input("Enter your choice: ")
    if inp == "1":
        try:
            id = input("Enter the ID: ")
            parentId = input("Enter the parent ID: ")
            title = input("Enter the title: ")
            metaTitle = input("Enter the meta title: ")
            slug = input("Enter the slug: ")
            content = input("Enter the content: ")

            VALUES = "(`parentId`, `title`, `metaTitle`, `slug`, `content`) values('{}','{}','{}','{}','{}')".format(parentId,title,metaTitle,slug,content)
            insert_data(con,"category",VALUES)

        except mysql.connector.IntegrityError:
            con.rollback()
            system("clear||cls")
            print("The Value Entered is DUPLICATE or Tampers the INTEGRITY of DataBase")
            category_table()
    elif inp == "2":
        cols = extract_column_names(con,"category")
        myTable = PrettyTable(cols)
        values = display_data(con,"category")
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)
        
        index = 1
        for i in cols[1:]:
            print(f"{index}. Update {i}",end='\n')
            index += 1

        inp = input("Enter your choice: ")    
        id = input("Enter the ID: ")

        if inp == "1":
            parentId_new = input("Enter your parent ID: ")
            update_data(con,"category",f"`parentId` = '{parentId_new}'",f"`id` = '{id}'")
        elif inp == "2":
            title_new = input("Enter your title: ")
            update_data(con,"category",f"`title` = '{title_new}'",f"`id` = '{id}'")
        elif inp == "3":
            metaTitle_new = input("Enter your meta title: ")
            update_data(con,"category",f"`metaTitle` = '{metaTitle_new}'",f"`id` = '{id}'")
        elif inp == "4":
            slug_new = input("Enter your slug: ")
            update_data(con,"category",f"`slug` = '{slug_new}'",f"`id` = '{id}'")
        elif inp == "5":
            content_new = input("Enter your content: ")
            update_data(con,"category",f"`content` = '{content_new}'",f"`id` = '{id}'")
        else:
            system("clear||cls")
            print("Invalid input!")
            category_table()
    elif inp == "3":
        cols = extract_column_names(con,"category")
        myTable = PrettyTable(cols)
        values = display_data(con,"category")
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)

        id = input("Enter ID of the user to be deleted: ")
        delete_data(con, "category", f"`id` = '{id}'")
    elif inp == "4":
        cols = extract_column_names(con,"category")
        index = 1
        for i in cols:
            print(f"{index}. Select by {i}",end='\n')
            index += 1
        inp = input("Enter your choice: ")     
        if inp == "1":
            id = input("Enter ID: ")
            values = search_data(con,"category",f"id = '{id}'")
        elif inp == "2":
            userId = input("Enter user ID: ")
            values = search_data(con,"category",f"`userId`='{userId}'")
        elif inp == "3":
            orderId = input("Enter order ID: ")
            values = search_data(con,"category",f"`orderId`='{orderId}'")
        elif inp == "4":
            firstName = input("Enter first name: ")
            values = search_data(con,"category",f"`firstName`='{firstName}'")
        elif inp == "5":
            middleName = input("Enter middle name: ")
            values = search_data(con,"category",f"`middleName`='{middleName}'")
        elif inp == "6":
            lastName = input("Enter last name: ")
            values = search_data(con,"category",f"`lastName`='{lastName}'")
        elif inp == "7":
            mobile = input("Enter mobile: ")
            values = search_data(con,"category",f"`mobile`='{mobile}'")
        elif inp == "8":
            email = input("Enter email: ")
            values = search_data(con,"category",f"`email`='{email}'")
        elif inp == "9":
            line1 = input("Enter line 1: ")
            values = search_data(con,"category",f"`line1`='{line1}'")
        elif inp == "10":
            line2 = input("Enter line 2: ")
            values = search_data(con,"category",f"`line2`='{line2}'")
        elif inp == "11":
            city = input("Enter city: ")
            values = search_data(con,"category",f"`city`='{city}'")
        elif inp == "12":
            province = input("Enter province: ")
            values = search_data(con,"category",f"`province`='{province}'")
        elif inp == "13":
            country = input("Enter country: ")
            values = search_data(con,"category",f"`country`='{country}'")
        elif inp == "14":
            createdAt = input("Enter created at: ")
            values = search_data(con,"category",f"`createdAt`='{createdAt}'")
        elif inp == "15":
            updatedAt = input("Enter updated at: ")
            values = search_data(con,"category",f"`updatedAt`='{updatedAt}'")
        else:
            system("clear||cls")
            print("Invalid Choice")

        cols = extract_column_names(con,"category")
        myTable = PrettyTable(cols)
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)
    elif inp == "5":
        cols = extract_column_names(con,"category")
        myTable = PrettyTable(cols)
        values = display_data(con,"category")
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)   

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
            con.rollback()
            system("clear||cls")
            print("Check if you have filled values in Order table first!")
            order_table()
            
    elif inp == "2":
        cols = extract_column_names(con,"address")
        myTable = PrettyTable(cols)
        values = display_data(con,"address")
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)
        
        index = 1
        for i in cols[1:-1]:
            print(f"{index}. Update {i}",end='\n')
            index += 1
        inp = input("Enter your choice: ")    
        id = input("Enter the ID: ")
        if inp == "1":
            userId_new = input("Enter your user ID: ")
            update_data(con,"address",f"`userId` = '{userId_new}'",f"`id` = '{id}'")
        elif inp == "2":
            orderId_new = input("Enter your order ID: ")
            update_data(con,"address",f"`orderId` = '{orderId_new}'",f"`id` = '{id}'")
        elif inp == "3":
            firstName_new = input("Enter your first name: ")
            update_data(con,"address",f"`firstName` = '{firstName_new}'",f"`id` = '{id}'")
        elif inp == "4":
            middleName_new = input("Enter your middle name: ")
            update_data(con,"address",f"`middleName` = '{middleName_new}'",f"`id` = '{id}'")
        elif inp == "5":
            lastName_new = input("Enter your last name: ")
            update_data(con,"address",f"`lastName` = '{lastName_new}'",f"`id` = '{id}'")
        elif inp == "6":
            mobile_new = input("Enter your mobile number: ")
            update_data(con,"address",f"`mobile` = '{mobile_new}'",f"`id` = '{id}'")
        elif inp == "7":
            email_new = input("Enter Email ID: ")
            update_data(con,"address",f"`email` = '{email_new}'",f"`id` = '{id}'")
        elif inp == "8":
            line1_new = input("Enter your line 1: ")
            update_data(con,"address",f"`line1` = '{line1_new}'",f"`id` = '{id}'")
        elif inp == "9":
            line2_new = input("Enter your line 2: ")
            update_data(con,"address",f"`line2` = '{line2_new}'",f"`id` = '{id}'")
        elif inp == "10":
            city_new = input("Enter your city: ")
            update_data(con,"address",f"`city` = '{city_new}'",f"`id` = '{id}'")
        elif inp == "11":
            province_new = input("Enter your province: ")
            update_data(con,"address",f"`province` = '{province_new}'",f"`id` = '{id}'")
        elif inp == "12":
            country_new = input("Enter your country: ")
            update_data(con,"address",f"`country` = '{country_new}'",f"`id` = '{id}'")
        elif inp == "13":
            createdAt_new = input("Enter your created at: ")
            update_data(con,"address",f"`createdAt` = '{createdAt_new}'",f"`id` = '{id}'")
        else:
            system("clear||cls")
            print("Invalid input!")
            address_table()
        
        now = datetime.now()
        updated_at_new =  now.strftime("%Y-%m-%d %H:%M:%S")
        update_data(con,"address",f"`updatedAt`='{updated_at_new}'",f"`id`= {id}")
        con.commit()
        con.close()
    elif inp == "3":
        cols = extract_column_names(con,"address")
        myTable = PrettyTable(cols)
        values = display_data(con,"address")
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)

        id = input("Enter ID of the user to be deleted: ")
        delete_data(con, "address", f"`id` = '{id}'")
    elif inp == "4":
        cols = extract_column_names(con,"address")
        index = 1
        for i in cols:
            print(f"{index}. Select by {i}",end='\n')
            index += 1
        inp = input("Enter your choice: ")     
        if inp == "1":
            id = input("Enter ID: ")
            values = search_data(con,"address",id)
        elif inp == "2":
            userId = input("Enter user ID: ")
            values = search_data(con,"address",f"`userId`='{userId}'")
        elif inp == "3":
            orderId = input("Enter order ID: ")
            values = search_data(con,"address",f"`orderId`='{orderId}'")
        elif inp == "4":
            firstName = input("Enter first name: ")
            values = search_data(con,"address",f"`firstName`='{firstName}'")
        elif inp == "5":
            middleName = input("Enter middle name: ")
            values = search_data(con,"address",f"`middleName`='{middleName}'")
        elif inp == "6":
            lastName = input("Enter last name: ")
            values = search_data(con,"address",f"`lastName`='{lastName}'")
        elif inp == "7":
            mobile = input("Enter mobile: ")
            values = search_data(con,"address",f"`mobile`='{mobile}'")
        elif inp == "8":
            email = input("Enter email: ")
            values = search_data(con,"address",f"`email`='{email}'")
        elif inp == "9":
            line1 = input("Enter line 1: ")
            values = search_data(con,"address",f"`line1`='{line1}'")
        elif inp == "10":
            line2 = input("Enter line 2: ")
            values = search_data(con,"address",f"`line2`='{line2}'")
        elif inp == "11":
            city = input("Enter city: ")
            values = search_data(con,"address",f"`city`='{city}'")
        elif inp == "12":
            province = input("Enter province: ")
            values = search_data(con,"address",f"`province`='{province}'")
        elif inp == "13":
            country = input("Enter country: ")
            values = search_data(con,"address",f"`country`='{country}'")
        elif inp == "14":
            createdAt = input("Enter created at: ")
            values = search_data(con,"address",f"`createdAt`='{createdAt}'")
        elif inp == "15":
            updatedAt = input("Enter updated at: ")
            values = search_data(con,"address",f"`updatedAt`='{updatedAt}'")
        else:
            system("clear||cls")
            print("Invalid Choice")

        cols = extract_column_names(con,"address")
        myTable = PrettyTable(cols)
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)
    elif inp == "5":
        cols = extract_column_names(con,"address")
        myTable = PrettyTable(cols)
        values = display_data(con,"address")
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)       

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
