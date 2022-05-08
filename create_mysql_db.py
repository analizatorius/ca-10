import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="##Sqshinemylight")

my_cursor = mydb.cursor()

#commented out cuz it can create new db
my_cursor.execute("CREATE DATABASE wb_users")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)