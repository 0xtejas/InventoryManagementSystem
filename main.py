import mysql.connector as connector



if __name__ == '__main__':
    # TEST MYSQL CONNECTIONS
    con = connector.connect(
        host='localhost',
        user='root',
        passwd='root',
    )
    if con.is_connected():
        print('Connected to MySQL database')
    else:
        print('Connection failed')
