import sqlite3
import os

#This is in for testing purposes - Delete later ------
if os.path.exists("Theia.db"):
    os.remove("Theia.db")
    print("Script was ran before so removing previous db")
#---------------------------------------------


connection = sqlite3.connect("Theia.db")

cursor = connection.cursor()

with open("UserTable.sql", "r") as file:
    cursor.execute(file.read())

connection.commit()

#Take in user input -- input later to taken from UI 
name = input("Enter a your name: ")

age = input("Enter your age: ")

#input validation
while True: 
    try: 
        age = int(age)
        break
    except ValueError:
        age = input("Enter a valid age:")


emergencyNum = input("Enter an emergency contact number with no '-' or '()' : ")

while True:
    try:
        emergencyNum = int(emergencyNum)
        break
    except ValueError:
        emergencyNum = input("Invaild, add number with no dashes '-' or parenthesis'()' : ")



cursor.execute(f"INSERT INTO USERDATA(username,age,emergency_contact) VALUES(?,?,?)",(name,age,emergencyNum))

#Now test to see if the data was inserted properly 
cursor.execute(f"SELECT * FROM USERDATA WHERE username = '{name}'")
tableData = cursor.fetchone()

if tableData[0] == None:
    print("Inserting username failed")
elif tableData[0] == name:
    print("Inserting username sucess")

if tableData[1] == None:
    print("Inserting age failed")
elif tableData[1] == age:
    print("Inserting age sucess")

if tableData[2] == None:
    print("Inserting emergency number failed")
elif tableData[2] == emergencyNum:
    print("Inserting emergency number sucess")


connection.commit()
connection.close()