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
    stmt = "INSERT INTO `{table_name}` {values}"
    cursor.execute(stmt.format(table_name=table_name,values=values))
    con.commit()
    
def display_data(con,table_name):
    cursor = con.cursor()
    stmt = "SELECT * FROM `{table_name}`"
    cursor.execute(stmt.format(table_name=table_name))
    rows = cursor.fetchall()
    return rows



def update_data(con,table_name,values,where):
    cursor = con.cursor()
    stmt = "UPDATE `{table_name}` SET {values} WHERE {where}"
    cursor.execute(stmt.format(table_name=table_name,values=values,where=where))
    con.commit()

def delete_data(con,table_name,where):
    cursor = con.cursor()
    stmt = "DELETE FROM `{table_name}` WHERE {where}"
    cursor.execute(stmt.format(table_name=table_name,where=where))
    con.commit()
   

def search_data(cursor,table_name,where):
    cursor = con.cursor()
    stmt = "SELECT * FROM `{table_name}` WHERE {where}"  
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
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database=DB_NAME,
        buffered=True
    )
    if options == 1:
        print(common_menu_banner.format("Product Table"))
        inp = input("Enter your choice: ")
        if inp == "1":
            title = input("Enter title: ")
            type_val = input("Enter type: ")
            now = datetime.now()
            createdAt = now.strftime("%Y-%m-%d %H:%M:%S")
            content = input("Enter content: ")


            values = "(`title`, `type`, `createdAt`, `content`) values('{}','{}','{}','{}')".format(title,type_val,createdAt,content)
            insert_data(con,"product",values)
        elif inp == "2":
            cols = extract_column_names(con,"product")
            myTable = PrettyTable(cols)
            values = display_data(con,"product")

            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)

            index = 1
            cols.pop(4)
            for i in cols[1:]:
                print(f"{index}. Update {i}",end='\n')
                index += 1
            inp = input("Enter your choice: ")    
            id = input("Enter the ID: ")

            if inp == "1":
                title_new = input("Enter Title: ")
                update_data(con,"product",f"`title` = '{title_new}'",f"`id` = '{id}'")
            elif inp == "2":
                type_new = input("Enter Type: ")
                update_data(con,"product",f"`type` = '{type_new}'",f"`id` = '{id}'")
            elif inp == "3":
                createdAt_new = input("Enter Created At: ")
                update_data(con,"product",f"`createdAt` = '{createdAt_new}'",f"`id` = '{id}'")
            elif inp == "4":
                content_new = input("Enter Content: ")
                update_data(con,"product",f"`content` = '{content_new}'",f"`id` = '{id}'")
            else:
                system("clear||cls")
                print("Invalid Choice")
                product_table()

            now = datetime.now()
            updatedAt = now.strftime("%Y-%m-%d %H:%M:%S")   
            update_data(con,"product",f"`updatedAt` = '{updatedAt}'",f"`id` = '{id}'")
            con.commit()
            con.close()
        
    elif options == 2:
        print(common_menu_banner.format("Product Category Table"))

    
def order_table(options):
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database=DB_NAME,
        buffered=True
    )
    if options == 1:
        print(common_menu_banner.format("Order"))
        inp = input("Enter your choice: ")
        if inp == "1":
            try:
                userId = input("Enter User ID: ")
                type_value = input("Enter Type: ")
                status = input("Enter Status: ")
                subTotal = input("Enter Sub Total: ")
                itemDiscount = input("Enter Item Discount: ")
                tax = input("Enter Tax: ")
                shipping = input("Enter Shipping: ")
                total = float(subTotal) + float(tax) + float(shipping) - float(itemDiscount)
                promo = input("Enter Promo: ")
                discount = input("Enter Discount: ")
                if discount == "":
                    discount = 0
                grandTotal = float(total) - float(discount)
                now = datetime.now()
                createdAt = now.strftime("%Y-%m-%d %H:%M:%S")
                content = input("Enter Content: ")
                values = "(`userId`, `type`, `status`, `subTotal`, `itemDiscount`, `tax`, `shipping`, `total`, `promo`, `discount`, `grandTotal`, `createdAt`, `updatedAt`, `content`) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',NULL,'{}')".format(userId,type_value,status,subTotal,itemDiscount,tax,shipping,total,promo,discount,grandTotal,createdAt,content)
                insert_data(con,"order",values)
            except mysql.exceptions.IntegrityError:
                print("Check if the User ID exist in User Table")
            con.commit()
            con.close()

        elif inp == "2":
            cols = extract_column_names(con,"order")
            myTable = PrettyTable(cols)
            values = display_data(con,"order")
    
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)

            index = 1
            cols.pop(13)
            for i in cols[1:-1]:
                print(f"{index}. Update {i}",end='\n')
                index += 1
            inp = input("Enter your choice: ")    
            id = input("Enter the ID: ")
            if inp == "1":
                userId_new = input("Enter your user ID: ")
                update_data(con,"order",f"`userId` = '{userId_new}'",f"`id` = '{id}'")
            elif inp == "2":
                type_new = input("Enter your type: ")
                update_data(con,"order",f"`type` = '{type_new}'",f"`id` = '{id}'")
            elif inp == "3":
                status_new = input("Enter your status: ")
                update_data(con,"order",f"`status` = '{status_new}'",f"`id` = '{id}'")
            elif inp == "4":
                subTotal_new = input("Enter your sub total: ")
                update_data(con,"order",f"`subTotal` = '{subTotal_new}'",f"`id` = '{id}'")
                for i in values:
                    if int(id) == i[0]:
                        total_new = float(subTotal_new) - float(i[5]) + float(i[6]) + float(i[7])
                        update_data(con,"order",f"`total` = '{total_new}'",f"`id` = '{id}'")
                        grandTotal_new = float(total_new) - float(i[10])
                        update_data(con,"order",f"`grandTotal` = '{grandTotal_new}'",f"`id` = '{id}'")

            elif inp == "5":
                itemDiscount_new = input("Enter your item discount: ")
                update_data(con,"order",f"`itemDiscount` = '{itemDiscount_new}'",f"`id` = '{id}'")
                for i in values:
                    if int(id) == i[0]:
                        total_new = float(i[4]) - float(itemDiscount_new) + float(i[6]) + float(i[7])
                        update_data(con,"order",f"`total` = '{total_new}'",f"`id` = '{id}'")
                        grandTotal_new = float(total_new) - float(i[10])
                        update_data(con,"order",f"`grandTotal` = '{grandTotal_new}'",f"`id` = '{id}'")
            elif inp == "6":
                tax_new = input("Enter your tax: ")
                update_data(con,"order",f"`tax` = '{tax_new}'",f"`id` = '{id}'")
                for i in values:
                    if int(id) == i[0]:
                        total_new = float(i[4]) - float(i[5]) + float(tax_new) + float(i[7])
                        update_data(con,"order",f"`total` = '{total_new}'",f"`id` = '{id}'")
                        grandTotal_new = float(total_new) - float(i[10])
                        update_data(con,"order",f"`grandTotal` = '{grandTotal_new}'",f"`id` = '{id}'")
            elif inp == "7":
                shipping_new = input("Enter your shipping: ")
                update_data(con,"order",f"`shipping` = '{shipping_new}'",f"`id` = '{id}'")
                for i in values:
                    if int(id) == i[0]:
                        total_new = float(i[4]) - float(i[5]) + float(i[6]) + float(shipping_new)
                        update_data(con,"order",f"`total` = '{total_new}'",f"`id` = '{id}'")
                        grandTotal_new = float(total_new) - float(i[10])
                        update_data(con,"order",f"`grandTotal` = '{grandTotal_new}'",f"`id` = '{id}'")
            elif inp == "8":
                subTotal_new = float(input("Enter your sub total: "))
                itemDiscount_new = float(input("Enter your item discount: "))
                tax_new = float(input("Enter your tax: "))
                shipping_new = float(input("Enter your shipping: "))
                total_new = float(subTotal_new) - float(itemDiscount_new) + float(tax_new) + float(shipping_new)
                update_data(con,"order",f"`subTotal` = '{subTotal_new}', `itemDiscount` = '{itemDiscount_new}', `tax` = '{tax_new}', `shipping` = '{shipping_new}', `total` = '{total_new}'",f"`id` = '{id}'")
                for i in values:
                    if int(id) == i[0]:
                        grandTotal_new = float(total_new) - float(i[10])
                        update_data(con,"order",f"`grandTotal` = '{grandTotal_new}'",f"`id` = '{id}'")
            elif inp == "9":
                promo_new = input("Enter your promo: ")
                discount_new = input("Enter your discount: ")
                grandTotal_new = values[int(id)][8] - float(discount_new)
                update_data(con,"order",f"`promo` = '{promo_new}', `discount` = '{discount_new}', `grandTotal` = '{grandTotal_new}'",f"`id` = '{id}'")
            elif inp == "10":
                discount_new = input("Enter your discount: ")
                grandTotal_new = values[int(id)][8] - float(discount_new)
                promo_new = input("Enter your promo: ")
                update_data(con,"order",f"`promo` = '{promo_new}', `discount` = '{discount_new}', `grandTotal` = '{grandTotal_new}'",f"`id` = '{id}'")

            elif inp == "11":
                subTotal_new = input("Enter your sub total: ")
                itemDiscount_new = input("Enter your item discount: ")
                tax_new = input("Enter your tax: ")
                shipping_new = input("Enter your shipping: ")
                total_new = float(subTotal_new) - float(itemDiscount_new) + float(tax_new) + float(shipping_new)
                promo_new = input("Enter your promo: ")
                discount_new = input("Enter your discount: ")
                grandTotal_new = float(total_new) - float(discount_new)
                update_data(con,"order",f"`subTotal` = '{subTotal_new}', `itemDiscount` = '{itemDiscount_new}', `tax` = '{tax_new}', `shipping` = '{shipping_new}', `total` = '{total_new}', `promo` = '{promo_new}', `discount` = '{discount_new}', `grandTotal` = '{grandTotal_new}'",f"`id` = '{id}'")

            elif inp == "12":
                createdAt_new = input("Enter new Created At: ")
                update_data(con,"order",f"`createdAt` = '{createdAt_new}'",f"`id` = '{id}'")
            
            now = datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            update_data(con,"order",f"`updatedAt` = '{now}'",f"`id` = '{id}'")

        elif inp == "3":
            cols = extract_column_names(con,"order")
            myTable = PrettyTable(cols)
            values = display_data(con,"order")
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)

            id = input("Enter ID: ")
            delete_data(con,"order",f"`id` = '{id}'")
        
        elif inp == "4":
            cols = extract_column_names(con,"order")
            index = 1
            for i in cols:
                print(f"{index}. Select by {i}",end='\n')
                index += 1
            inp = input("Enter your choice: ")
            if inp == "1":
                Id = input("Enter ID: ")
                values = search_data(con,"order",f"`id` = '{Id}'")
            elif inp == "2":
                userId = input("Enter userId: ")
                values = search_data(con,"order",f"`userId` = '{userId}'")
            elif inp == "3":
                type_val = input("Enter the type: ")
                values = search_data(con,"order",f"`type` = '{type_val}'")
            elif inp == "4":
                status = input("Enter the status: ")
                values = search_data(con,"order",f"`status` = '{status}'")
            elif inp == "5":
                subTotal = input("Enter subTotal: ")
                values = search_data(con,"order",f"`subTotal` = '{subTotal}'")
            elif inp == "6":
                itemDiscount = input("Enter itemDiscount: ")
                values = search_data(con,"order",f"`itemDiscount` = '{itemDiscount}'")
            elif inp == "7":
                tax = input("Enter tax: ")
                values = search_data(con,"order",f"`tax` = '{tax}'")
            elif inp == "8":
                shipping = input("Enter shipping: ")
                values = search_data(con,"order",f"`shipping` = '{shipping}'")
            elif inp == "9":
                total = input("Enter total: ")
                values = search_data(con,"order",f"`total` = '{total}'")
            elif inp == "10":
                promo = input("Enter promo: ")
                values = search_data(con,"order",f"`promo` = '{promo}'")
            elif inp == "11":
                discount = input("Enter discount: ")
                values = search_data(con,"order",f"`discount` = '{discount}'")
            elif inp == "12":
                grandTotal = input("Enter grandTotal: ")
                values = search_data(con,"order",f"`grandTotal` = '{grandTotal}'")
            elif inp == "13":
                createdAt = input("Enter createdAt: ")
                values = search_data(con,"order",f"`createdAt` = '{createdAt}'")
            elif inp == "14":
                updatedAt = input("Enter updatedAt: ")
                values = search_data(con,"order",f"`updatedAt` = '{updatedAt}'")
            elif inp == "15":
                content = input("Enter content: ")
                values = search_data(con,"order",f"`content` = '{content}'")
            else:
                system("clear||cls")
                print("Invalid input!")
                transaction_table()
            
            cols = extract_column_names(con,"order")
            myTable = PrettyTable(cols)
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)
    
        elif inp == "5":
            cols = extract_column_names(con,"order")
            myTable = PrettyTable(cols)
            values = display_data(con,"order")
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)   
        
    
    elif options == 2:
        print(common_menu_banner.format("Order Item"))
        inp = input("Enter your choice: ")
        if inp == "1":
            try:
                productId = int(input("Enter the product ID: "))
                itemId = int(input("Enter the item ID: "))
                orderId = int(input("Enter the order ID: "))
                sku = str(input("Enter the sku: "))
                price = float(input("Enter the price: "))
                discount = float(input("Enter the discount: "))
                quantity = int(input("Enter the quantity: "))
                now = datetime.now()
                createdAt = now.strftime("%Y-%m-%d %H:%M:%S")
                values = "(`productId`, `itemId`, `orderId`, `sku`, `price`, `discount`, `quantity`, `createdAt`, `updatedAt`) values('{}','{}','{}','{}','{}','{}','{}','{}',NULL);".format(productId,itemId,orderId,sku,price,discount,quantity,createdAt)
            
                insert_data(con,"order_item",values)
            except mysql.connector.IntegrityError:
                print("Check if the Product/Item/Order ID exist in Product/Item/Order Table")
        elif inp == "2":
            cols = extract_column_names(con,"order_item")
            myTable = PrettyTable(cols)
            values = display_data(con,"order_item")
    
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
                try:
                    productId_new = int(input("Enter the product ID: "))
                    update_data(con,"order_item",f"`productId` = '{productId_new}'",f"`id` = '{id}'")
                except mysql.connector.IntegrityError:
                    print("Check if the Product ID exist in Product table")
            elif inp == "2":
                try:
                    itemId_new = int(input("Enter the item ID: "))
                    update_data(con,"order_item",f"`itemId` = '{itemId_new}'",f"`id` = '{id}'")
                except mysql.connector.IntegrityError:
                    print("Check if the Item ID exist in Item table")
            elif inp == "3":
                try:
                    orderId_new = int(input("Enter the order ID: "))
                    update_data(con,"order_item",f"`orderId` = '{orderId_new}'",f"`id` = '{id}'")
                except mysql.connector.IntegrityError:
                    print("Check if the Order ID exist in Order table")
            elif inp == "4":
                sku_new = str(input("Enter the sku: "))
                update_data(con,"order_item",f"`sku` = '{sku_new}'",f"`id` = '{id}'")
            elif inp == "5":
                price_new = float(input("Enter the price: "))
                update_data(con,"order_item",f"`price` = '{price_new}'",f"`id` = '{id}'")
            elif inp == "6":
                discount_new = float(input("Enter the discount: "))
                update_data(con,"order_item",f"`discount` = '{discount_new}'",f"`id` = '{id}'")
            elif inp == "7":
                quantity_new = int(input("Enter the quantity: "))
                update_data(con,"order_item",f"`quantity` = '{quantity_new}'",f"`id` = '{id}'")
            elif inp == "8":
                createdAt = input("Enter the createdAt: ")
                update_data(con,"order_item",f"`createdAt` = '{createdAt}'",f"`id` = '{id}'")
            
            now = datetime.now()
            updatedAt = now.strftime("%Y-%m-%d %H:%M:%S")
            update_data(con,"order_item",f"`updatedAt` = '{updatedAt}'",f"`id` = '{id}'")
        elif inp == "3":
            cols = extract_column_names(con,"order_item")
            myTable = PrettyTable(cols)
            values = display_data(con,"order_item")
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)

            id = input("Enter ID: ")
            delete_data(con,"order_item",f"`id` = '{id}'")
        elif inp == "4":
            cols = extract_column_names(con,"order_item")
            index = 1
            for i in cols:
                print(f"{index}. Select by {i}",end='\n')
                index += 1
            inp = input("Enter your choice: ")
            if inp == "1":
                id = input("Enter the ID: ")
                values = search_data(con,"order_item",f"`id` = '{id}'")
            elif inp == "2":
                productId = int(input("Enter the product ID: "))
                values = search_data(con,"order_item",f"`productId` = '{productId}'")
            elif inp == "3":
                itemId = int(input("Enter the item ID: "))
                values = search_data(con,"order_item",f"`itemId` = '{itemId}'")
            elif inp == "4":
                orderId = int(input("Enter the order ID: "))
                values = search_data(con,"order_item",f"`orderId` = '{orderId}'")
            elif inp == "5":
                sku = str(input("Enter the sku: "))
                values = search_data(con,"order_item",f"`sku` = '{sku}'")
            elif inp == "6":
                price = float(input("Enter the price: "))
                values = search_data(con,"order_item",f"`price` = '{price}'")
            elif inp == "7":
                discount = float(input("Enter the discount: "))
                values = search_data(con,"order_item",f"`discount` = '{discount}'")
            elif inp == "8":
                quantity = int(input("Enter the quantity: "))
                values = search_data(con,"order_item",f"`quantity` = '{quantity}'")
            elif inp == "9":
                createdAt = input("Enter the createdAt: ")
                values = search_data(con,"order_item",f"`createdAt` = '{createdAt}'")
            elif inp == "10":
                updatedAt = input("Enter the updatedAt: ")
                values = search_data(con,"order_item",f"`updatedAt` = '{updatedAt}'")
            else:
                system("clear||cls")
                print("Invalid Input")
            
            cols = extract_column_names(con,"order_item")
            myTable = PrettyTable(cols)
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)
        elif inp == "5":
            cols = extract_column_names(con,"order_item")
            myTable = PrettyTable(cols)
            values = display_data(con,"order_item")
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)   


def item_table(options):
    if options == 1:
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database=DB_NAME,
            buffered=True
        )    
        print(common_menu_banner.format("Item"))
        inp = input("Enter your choice: ")
        if inp == "1":
            try:
                product_id = input("Enter Product ID: ")
                brand_id = input("Enter Brand ID: ")
                supplier_id = input("Enter Supplier ID: ")
                orderId = input("Enter order ID:")
                sku = input("Enter SKU: ")
                mrp = input("Enter the MRP: ")
                discount = input("Enter the Discount: ")
                price = input("Enter the Price: ")
                quantity = input("Enter the quantity: ")
                sold = input("Enter the sold: ")
                available = input("Enter the available: ")
                defective = input("Enter the defective: ")
                createdBy = input("Enter the createdBy ID: ")
                updatedBy = input("Enter the updatedBy ID: ")
                now = datetime.now()
                createdAt = now.strftime("%Y-%m-%d %H:%M:%S")
                values ="(`productId`, `brandId`, `supplierId`, `orderId`, `sku`, `mrp`, `discount`, `price`, `quantity`, `sold`, `available`, `defective`, `createdBy`, `updatedBy`, `createdAt`, `updatedAt`) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',NULL) ".format(product_id,brand_id,supplier_id,orderId,sku,mrp,discount,price,quantity,sold,available,defective,createdBy,updatedBy,createdAt)
                insert_data(con,"item",values)

            except mysql.connector.IntegrityError:
                print("Please check if your Product/Brand/Supplier(User)/Order table are filled and the ID you mentioned is aligining with the table")

        elif inp == "2":
            cols = extract_column_names(con,"item")
            myTable = PrettyTable(cols)
            values = display_data(con,"item")
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)
            index = 1

            for i in cols[1:-2]:
                print(f"{index}. Update {i}",end='\n')
                index += 1     
            inp = input("Enter your choice: ")
            id = input("Enter the ID: ")
            if inp == "1":
                try:
                    productId_new = input("Enter the new product ID: ")
                    update_data(con,"item",f"`userId` = '{productId_new}'",f"`id` = '{id}'")
                except mysql.connector.IntegrityError:
                    print("Please check if your Product/Brand/Supplier(User)/Order table are filled and the ID you mentioned is aligining with the table")
            elif inp == "2":
                try:
                    brandId_new = input("Enter the new brand ID: ")
                    update_data(con,"item",f"`brandId` = '{brandId_new}'",f"`id` = '{id}'")
                except mysql.connector.IntegrityError:
                    print("Please check if your Brand table is filled and the ID you mentioned is aligining with the table")
            elif inp == "3":
                try:
                    supplierId_new = input("Enter the new supplier ID: ")
                    update_data(con,"item",f"`supplierId` = '{supplierId_new}'",f"`id` = '{id}'")
                except mysql.connector.IntegrityError:
                    print("Please check if your Supplier table is filled and the ID you mentioned is aligining with the table")
            elif inp == "4":
                try:
                    orderId_new = input("Enter the new order ID: ")
                    update_data(con,"item",f"`orderId` = '{orderId_new}'",f"`id` = '{id}'")
                except mysql.connector.IntegrityError:
                    print("Please check if your Order table is filled and the ID you mentioned is aligining with the table")
            elif inp == "5":
                sku_new = input("Enter the new SKU: ")
                update_data(con,"item",f"`sku` = '{sku_new}'",f"`id` = '{id}'")
            elif inp == "6":
                mrp_new = input("Enter the new MRP: ")
                update_data(con,"item",f"`mrp` = '{mrp_new}'",f"`id` = '{id}'")
            elif inp == "7":
                discount_new = input("Enter the new Discount: ")
                update_data(con,"item",f"`discount` = '{discount_new}'",f"`id` = '{id}'")
            elif inp == "8":
                price_new = input("Enter the new Price: ")
                update_data(con,"item",f"`price` = '{price_new}'",f"`id` = '{id}'")
            elif inp == "9":
                quantity_new = input("Enter the new quantity: ")
                update_data(con,"item",f"`quantity` = '{quantity_new}'",f"`id` = '{id}'")
            elif inp == "10":
                sold_new = input("Enter the new sold: ")
                update_data(con,"item",f"`sold` = '{sold_new}'",f"`id` = '{id}'")
            elif inp == "11":
                available_new = input("Enter the new available: ")
                update_data(con,"item",f"`available` = '{available_new}'",f"`id` = '{id}'")
            elif inp == "12":
                defective_new = input("Enter the new defective: ")
                update_data(con,"item",f"`defective` = '{defective_new}'",f"`id` = '{id}'")
            elif inp == "13":
                createdBy_new = input("Enter the new createdBy ID: ")
                update_data(con,"item",f"`createdBy` = '{createdBy_new}'",f"`id` = '{id}'")
            elif inp == "14":
                updatedBy_new = input("Enter the new updatedBy ID: ")
                update_data(con,"item",f"`updatedBy` = '{updatedBy_new}'",f"`id` = '{id}'")

            now = datetime.now()
            updatedAt = now.strftime("%Y-%m-%d %H:%M:%S")
            update_data(con,"item",f"`updatedAt` = '{updatedAt}'",f"`id` = '{id}'")

        elif inp == "3":
            cols = extract_column_names(con,"item")
            myTable = PrettyTable(cols)
            values = display_data(con,"item")
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)

            id = input("Enter ID to be deleted: ")
            delete_data(con, "item", f"`id` = '{id}'")

        elif inp == "4":
            cols = extract_column_names(con,"item")
            myTable = PrettyTable(cols)
            values = display_data(con,"item")
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)
            index = 1

            for i in cols:
                print(f"{index}. Update {i}",end='\n')
                index += 1
            inp = input("Enter your choice: ")     
            if inp == "1":
                id = input("Enter the ID: ")
                values = search_data(con,"item",f"`id` = '{id}'")
            elif inp == "2":
                productId = input("Enter the product ID: ")
                values = search_data(con,"item",f"`userId` = '{productId}'")
            elif inp == "3":
                brandId = input("Enter the brand ID: ")
                values = search_data(con,"item",f"`brandId` = '{brandId}'")
            elif inp == "4":
                supplierId = input("Enter the supplier ID: ")
                values = search_data(con,"item",f"`supplierId` = '{supplierId}'")
            elif inp == "5":
                orderId = input("Enter the order ID: ")
                values = search_data(con,"item",f"`orderId` = '{orderId}'")
            elif inp == "6":
                sku = input("Enter the SKU: ")
                values = search_data(con,"item",f"`sku` = '{sku}'")
            elif inp == "7":
                mrp = input("Enter the MRP: ")
                values = search_data(con,"item",f"`mrp` = '{mrp}'")
            elif inp == "8":
                discount = input("Enter the Discount: ")
                values = search_data(con,"item",f"`discount` = '{discount}'")
            elif inp == "9":
                price = input("Enter the Price: ")
                values = search_data(con,"item",f"`price` = '{price}'")
            elif inp == "10":
                quantity = input("Enter the quantity: ")
                values = search_data(con,"item",f"`quantity` = '{quantity}'")
            elif inp == "11":
                sold = input("Enter the sold: ")
                values = search_data(con,"item",f"`sold` = '{sold}'")
            elif inp == "12":
                available = input("Enter the available: ")
                values = search_data(con,"item",f"`available` = '{available}'")
            elif inp == "13":
                defective = input("Enter the defective: ")
                values = search_data(con,"item",f"`defective` = '{defective}'")
            elif inp == "14":
                createdBy = input("Enter the createdBy ID: ")
                values = search_data(con,"item",f"`createdBy` = '{createdBy}'")
            elif inp == "15":
                updatedBy = input("Enter the updatedBy ID: ")
                values = search_data(con,"item",f"`updatedBy` = '{updatedBy}'")
            elif inp == "16":
                createdAt = input("Enter the createdAt: ")
                values = search_data(con,"item",f"`createdAt` = '{createdAt}'")
            elif inp == "17":
                updatedAt = input("Enter the updatedAt: ")
                values = search_data(con,"item",f"`updatedAt` = '{updatedAt}'")
            else:
                system("clear||cls")
                print("Invalid Choice")

            cols = extract_column_names(con,"item")
            myTable = PrettyTable(cols)
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)
        
        elif inp == "5":
            cols = extract_column_names(con,"item")
            myTable = PrettyTable(cols)
            values = display_data(con,"item")
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)

    elif options == 2:
        con = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database=DB_NAME,
            buffered=True
        )    
        print(common_menu_banner.format("Brand"))
        inp = input("Enter your choice: ")
        if inp == "1":
            title = input("Enter the title: ")
            now = datetime.now()
            createdAt = now.strftime("%Y-%m-%d %H:%M:%S")
            
            values = "(`title`, `createdAt`, `updatedAt`) values ('{}','{}',NULL)".format(title,createdAt)
            insert_data(con,"brand",values)
        elif inp == "2":
            cols = extract_column_names(con,"brand")
            myTable = PrettyTable(cols)
            values = display_data(con,"brand")
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
                title_new = input("Enter your Title: ")    
                update_data(con,"brand",f"`title` = '{title_new}'",f"`id` = '{id}'")    
            elif inp == "2":
                createdAt_new = input("Enter your createdAt: ")
                update_data(con,"brand",f"`createdAt` = '{createdAt_new}'",f"`id` = '{id}'")
            
            now = datetime.now()
            updatedAt = now.strftime("%Y-%m-%d %H:%M:%S")
            update_data(con,"brand",f"`updatedAt` = '{updatedAt}'",f"`id` = '{id}'")

        elif inp == "3":
            cols = extract_column_names(con,"brand")
            myTable = PrettyTable(cols)
            values = display_data(con,"brand")
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)

            id = input("Enter ID to be deleted: ")
            delete_data(con, "brand", f"`id` = '{id}'")
        
        elif inp == "4":
            cols = extract_column_names(con,"brand")
            index = 1
            for i in cols:
                print(f"{index}. Select by {i}",end='\n')
                index += 1
            inp = input("Enter your choice: ")
            if inp == "1":
                id = input("Enter ID: ")
                values = search_data(con,"brand",f"`id` = '{id}'")
            elif inp == "2":
                title = input("Enter the title: ")
                values = search_data(con,"brand",f"`title` = '{title}'")
            elif inp == "3":
                createdAt = input("Enter the createdAt: ")
                values = search_data(con,"brand",f"`createdAt` = '{createdAt}'")
            elif inp == "4":
                updatedAt = input("Enter the updatedAt: ")
                values = search_data(con,"brand",f"`updatedAt` = '{updatedAt}'")
            else:
                system("clear||cls")
                print("Invalid Choice")     

            cols = extract_column_names(con,"brand")
            myTable = PrettyTable(cols)
            if len(values) != 0:
                for i in values:
                    myList = list(i)
                    myTable.add_row(myList)
                print(myTable)            
            else:
                print("No data found")

        elif inp == "5":
            cols = extract_column_names(con,"brand")
            myTable = PrettyTable(cols)
            values = display_data(con,"brand")
            for i in values:
                myList = list(i)
                myTable.add_row(myList)
            print(myTable)
        
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

            values = "(`userId`, `orderId`, `code`, `type`, `mode`, `status`, `createdAt`) values('{}','{}','{}','{}','{}','{}','{}')".format(userId,orderId,code,type,mode,status,createdAt)
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

    elif inp == "3":
        cols = extract_column_names(con,"transaction")
        myTable = PrettyTable(cols)
        values = display_data(con,"transaction")
        for i in values:
            myList = list(i)
            myTable.add_row(myList)
        print(myTable)

        id = input("Enter ID: ")
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
    cursor.execute("SELECT * FROM `{}`".format(table_name))
    field_names = [i[0] for i in cursor.description]
    return field_names


def menu():
    print("""
    1.  User Table
    2.  Product Table
    3.  Product Category Table
    4.  Order Table
    5.  Order Item Table
    6.  Item Table
    7.  Brand Table
    8.  Transaction Table
    9.  Address Table
    10. Category Table
    11. Exit 
    """)
    inp = input("Enter your choice: ")
    if inp == "1":
        user_table()
    elif inp == "2":
        product_table(1)
    elif inp == "3":
        product_table(2)
    elif inp == "4":
        order_table(1)
    elif inp == "5":
        order_table(2)
    elif inp == "6":
        item_table(1)
    elif inp == "7":
        item_table(2)
    elif inp == "8":
        transaction_table()
    elif inp == "9":
        address_table()
    elif inp == "10":
        category_table()
    elif inp == "11":
        exit()

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
