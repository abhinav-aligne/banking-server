# Install Sql library with using the below script into the environment folder
# pip install mysql-connector-python
import mysql.connector as SQL
import procedual 
from banking import BankAccount


try:
    conn = SQL.connect(
        user ='root',
        password = "Aligne",
        host = "localhost",
        port = 3306
    )
except Exception as e:
    print("cannot connect")
else:
    print("connected")

cursor = conn.cursor()


