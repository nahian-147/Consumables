# Consumables

Requirements :

1. Python3
2. rich (python module)
3. MySQL
4. Ubuntu or any other Debian Linux

How to Setup : 

1. Install all the requirements and initialize the database into mysql server using "cons.sql" file.
2. Before running myConsumes.py edit the host, username, and password by  the following :

db = mysql.connector.connect(
        host='$Your_Host_Name$',
        user='your_User_Name',
        password='Your_Password',
        database='CONSUMABLES')

3. After editing the source code run the program using "python3 myConsumes.py"

DONE !
