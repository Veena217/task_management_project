import mysql.connector

try:
    connection = mysql.connector.connect(
        host='161.97.186.196',
        user='vjit',
        password='Str0ngP@ssw0rd!',
        database='task_management'
    )
    if connection.is_connected():
        print("Connection successful")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if connection.is_connected():
        connection.close()
